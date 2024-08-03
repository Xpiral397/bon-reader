from rest_framework import serializers, status
from .models import User
from djoser import email
from .utilis import generate_6_digit_code
from djoser.serializers import PasswordResetConfirmSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# User.objects.all().delete()


class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    code = serializers.CharField()

    def validate(self, attrs):
        code = attrs.get("code")
        password = attrs.get("new_password")
        user = User.objects.filter(reset_code=code).first()
        if not user:
            raise serializers.ValidationError("Invalid reset code")
        user.set_password(password)
        user.reset_code = ""
        user.save()
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ref_name = 'user-serial'
        fields = ["id", "email", "first_name", "last_name", "gender"]

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "gender", "password"]

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            gender=validated_data["gender"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    code = serializers.CharField()

    def validate(self, attrs):
        code = attrs.get("code")
        password = attrs.get("new_password")
        user = User.objects.filter(reset_code=code).first()
        if not user:
            raise serializers.ValidationError("Invalid reset code")
        user.set_password(password)
        user.reset_code = ""
        user.save()
        return attrs






class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "gender", "password"]

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            gender=validated_data["gender"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

