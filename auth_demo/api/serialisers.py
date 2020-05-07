"""API serialisers."""

from rest_framework import serializers
from django.contrib.auth.models import Group
from oauth2_provider.models import AccessToken
from auth_demo.models.user import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )


class AccessTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessToken
        fields = ("token", )


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class NonAutheticatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name",)