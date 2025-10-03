import logging
from .models import *
from celery import shared_task
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
logger = logging.getLogger(__name__)
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework_simplejwt.token_blacklist.models import *

def send_otp(email, task=None):
    if not email:
        raise ValueError("Email is required.")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return {"success": False, "message": "User not found."}
    

    otp = OTP.objects.filter(user__email=email).first()
    if otp and not otp.is_expired():
        return {"success": False, "message": "An OTP has already sent. Please check your email."}
    

    # Remove old OTP if exists
    OTP.objects.filter(user=user).delete()

    # Generate new OTP
    otp = OTP.generate_otp(user)

    subject = "Feet First OTP Verification"

    # Render HTML template (templates/email/otp_email.html)
    html_content = render_to_string("email/otp_email.html", {
        "otp": otp.otp,
        "task": task or "Verification",
        "user": user.name or user.email,
    })

    # Plain text fallback (for clients that don’t support HTML)
    text_content = f"""
    Your OTP Code From Feet First for {task or ''} is: {otp.otp}
    This OTP is valid for 3 minutes.
    If you did not request this, please ignore this email.
    """

    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return {"success": True, "message": f"OTP sent successfully for {task or 'Verification'}."}


def verify_otp(email, otp_code, max_attempts=3, lock_minutes=1):
    try:
        otp_obj = OTP.objects.filter(user__email=email).latest('created_at')
    except OTP.DoesNotExist:
        return {"success": False, "message": "Invalid OTP or email."}

    # Check expiry
    if otp_obj.is_expired():
        return {"success": False, "message": "OTP has expired."}

    # Check attempt limit
    if otp_obj.attempt_count >= max_attempts:
        if otp_obj.last_tried and otp_obj.last_tried + timedelta(minutes=lock_minutes) > timezone.now():
            remaining = int((otp_obj.last_tried + timedelta(minutes=lock_minutes) - timezone.now()).seconds)
            return {"success": False, "message": f"Too many attempts. Try again in {remaining} seconds."}
        else:
            otp_obj.attempt_count = 0  # reset after lock period

    # Verify OTP
    if otp_obj.otp != otp_code:
        otp_obj.attempt_count += 1
        otp_obj.last_tried = timezone.now()
        otp_obj.save()
        attempts_left = max_attempts - otp_obj.attempt_count
        return {"success": False, "message": f"Invalid OTP. You have {attempts_left} attempts left."}

    # OTP verified, activate user & delete OTP
    user = otp_obj.user
    user.is_active = True
    user.save()
    otp_obj.delete()

    return {"success": True, "message": "OTP verified successfully."}


@shared_task
def cleanup_expired_tokens():
    """
    Remove expired tokens from both OutstandingToken and BlacklistedToken tables.
    """
    now = timezone.now()

    # Remove expired BlacklistedTokens
    expired_blacklist = BlacklistedToken.objects.filter(token__expires_at__lt=now)
    blacklist_count = expired_blacklist.count()
    expired_blacklist.delete()

    # Remove expired OutstandingTokens
    expired_outstanding = OutstandingToken.objects.filter(expires_at__lt=now)
    outstanding_count = expired_outstanding.count()
    expired_outstanding.delete()

    logger.info(f"Expired cleanup done: {blacklist_count} blacklisted tokens removed, "
                f"{outstanding_count} outstanding tokens removed.")
    
@shared_task
def cleanup_expired_otps():
    """
    Remove expired OTP entries from the database.
    """
    now = timezone.now()
    expired_otps = OTP.objects.filter(created_at__lt=now - timedelta(minutes=10))
    count = expired_otps.count()
    expired_otps.delete()
    logger.info(f"Expired OTP cleanup done: {count} OTPs removed.")

@shared_task
def cleanup_old_deletion_requests():
    """
    Delete AccountDeletionRequest records that were confirmed
    more than 30 days ago.
    """
    threshold_date = timezone.now() - timedelta(days=30)
    deleted_count, _ = AccountDeletionRequest.objects.filter(
        deleted_at__lte=threshold_date
    ).delete()
    logger.info(f"Deleted {deleted_count} old deletion requests.")  