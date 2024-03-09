from rest_framework import serializers
from .models import User, UserConfirmation
from rest_framework.exceptions import ValidationError


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField(max_length=255)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)


class UserConfirmationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = UserConfirmation
        fields = ['code', 'email']