from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "password", "name", "bio", "image"]

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.pop("password")
        user = User(**validated_data)
        if email and not user.username:
            user.username = email.split("@")[0]   # auto-generate username
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        
        # First try to get the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")
        
        # Then authenticate with username (which might be same as email)
        user = authenticate(username=user.username, password=password)
        
        if not user:
            raise serializers.ValidationError("Invalid email or password")
            
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
            
        data["user"] = user
        return data