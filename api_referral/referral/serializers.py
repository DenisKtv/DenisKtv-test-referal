from rest_framework import serializers
from .models import UserProfile
import re
from django.core.exceptions import ValidationError


class SignUpSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=21)

    class Meta:
        model = UserProfile
        fields = ('phone_number', 'username')

    def validate_phone_number(self, phone_number):
        pattern = r'^\+?[0-9\-]+$'
        if not re.match(pattern, phone_number):
            raise ValidationError(
                'Телефон может состоять только из цифр и +-'
            )
        return phone_number


class SignInSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    verification_code = serializers.IntegerField(required=False)
