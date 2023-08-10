from rest_framework import serializers
from .models import UserProfile
from django.core.exceptions import ValidationError
import re


class SignUpSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=16)

    class Meta:
        model = UserProfile
        fields = ('phone_number',)

    def validate_phone_number(self, phone_number):
        pattern = r'^\+?[0-9\-]+$'
        if not re.match(pattern, phone_number):
            raise ValidationError(
                'Телефон может состоять только из цифр и +-'
            )
        return phone_number

    def create(self, validated_data):
        user_profile = UserProfile(**validated_data)
        user_profile.generate_invite_code()
        user_profile.save()
        return user_profile


class UserProfileSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=16)
    invite_code = serializers.CharField(max_length=6, required=True)

    def validate(self, data):
        phone_number = data['phone_number']
        invite_code = data['invite_code']

        user_profile = UserProfile.objects.filter(
            phone_number=phone_number
        ).first()
        if not user_profile:
            raise serializers.ValidationError(
                {'message': 'Такой номер не зарегистрирован'}
            )

        if user_profile.entered_invite_code:
            raise serializers.ValidationError(
                {'message': 'Вы уже активировали реферральный код.'}
            )

        if invite_code == user_profile.invite_code:
            raise serializers.ValidationError(
                {'message': 'Вы не можете использовать свой собственный '
                 'реферральный код.'}
            )

        if not UserProfile.objects.filter(invite_code=invite_code).exists():
            raise serializers.ValidationError(
                {'message': 'Введенный '
                 'реферральный код не существует.'}
                )

        return data


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('phone_number',)
