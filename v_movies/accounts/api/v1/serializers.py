from rest_framework import serializers
from rest_framework.validators import ValidationError
from accounts.models import User
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, attrs):
        phone_number_exists = User.objects.filter(phone_number=attrs["phone_number"])

        if phone_number_exists:
            raise ValidationError("Phone number has already been used")

        return super().validate(attrs)


class VerifySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
