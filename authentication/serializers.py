import re

from django.contrib.auth import authenticate

from rest_framework import serializers
from .models import User, BlacklistedToken


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'token', 'refresh_token']
        read_only_fields = ['token', 'refresh_token']

        extra_kwargs = {
            "password": {"write_only": True, }
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if not re.fullmatch(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}', data["password"]):
            raise serializers.ValidationError(
                'Password should contain capital, small letter and a number, larger than 8.'
            )
        else:
            return data


class LoginSerializer(serializers.Serializer):
    """
    Separate serializer for login
    Nothing to change in database
    """

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """
        Validate login data
        """

        email = data.get('email', None)
        password = data.get('password', None)

        # email and password cannot be None
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # try to find an existing user
        user = authenticate(username=email, password=password)

        # raise or return validated
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        else:
            return {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'token': user.token,
                'refresh_token': user.refresh_token,
            }


class LogoutSerializer(serializers.ModelSerializer):
    """
    Serializer for enter blacklisted token into database
    """
    class Meta:
        model = BlacklistedToken
        fields = ("token", )

