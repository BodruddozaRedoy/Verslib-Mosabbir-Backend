import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core", broker="redis://redis:6379/0")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

from celery.schedules import schedule

# Beat schedule
app.conf.beat_schedule.update({
    "cleanup-expired-tokens-daily": {
        "task": "Accounts.utils.cleanup_expired_tokens",
        "schedule": crontab(hour=0, minute=0),  # Daily at 12:00 AM
    },
    "cleanup-expired-otps": {
        "task": "Accounts.utils.cleanup_expired_otps",
        "schedule": schedule(3600.0),  # Every 60 minutes
    },
    "cleanup-deletion-requests-daily": {
        "task": "Accounts.utils.cleanup_old_deletion_requests",
        "schedule": crontab(hour=0, minute=0),  # run daily at midnight
    },
})

app.conf.timezone = "UTC"
