import random
import time

from django.core.cache import cache
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import (ReferralSerializer, SignUpSerializer,
                          UserProfileSerializer)
from .verification_service import VerificationService


class SignUpView(APIView):
    def generate_verification_code(self, phone_number):
        verification_code = random.randint(1000, 9999)
        cache.set(phone_number, verification_code, timeout=90)
        time.sleep(2)
        return verification_code

    def check_verification_code(self, phone_number, verification_code):
        cached_code = cache.get(phone_number)
        return cached_code == verification_code

    @swagger_auto_schema(
        operation_description='Получает номер телефона. Если это первый '
                              'запрос, то сохраняет в БД. Если нет, то '
                              'авторизует пользователя.',
        request_body=SignUpSerializer,
        responses={200: 'Успешно'}
    )
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        phone_number = serializer.validated_data['phone_number']
        verification_code = request.data.get('verification_code')

        if verification_code is None:
            verification_code = VerificationService.generate_verification_code(
                phone_number
            )
            return Response(
                {"verification_code": verification_code},
                status=status.HTTP_200_OK
            )

        if not VerificationService.check_verification_code(
            phone_number, verification_code
        ):
            return Response(
                {"message": "Код верификации неверен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_profile, created = UserProfile.objects.get_or_create(
            phone_number=phone_number
        )
        if created:
            user_profile.generate_invite_code()
            user_profile.save()
            message = 'Регистрация успешно пройдена'
        else:
            message = 'Успешная авторизация'

        return Response(
            {'message': message},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html')


class UserProfileView(APIView):

    @swagger_auto_schema(
        operation_description="Активирует инвайт-код.",
        request_body=UserProfileSerializer,
        responses={200: "Реферральный код успешно добавлен"}
    )
    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        phone_number = serializer.validated_data['phone_number']
        invite_code = serializer.validated_data['invite_code']

        user_profile = UserProfile.objects.get(phone_number=phone_number)
        referrer_profile = UserProfile.objects.get(invite_code=invite_code)

        user_profile.entered_invite_code = invite_code
        user_profile.activated_invite_code = referrer_profile
        user_profile.save()

        return Response(
            {'message': 'Реферральный код успешно добавлен'},
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description="Выводит личный инвайт-код.",
        responses={200: UserProfileSerializer}
    )
    def get(self, request, *args, **kwargs):
        phone_number = request.query_params.get('phone_number')
        if phone_number:
            user_profile = UserProfile.objects.filter(
                phone_number=phone_number
            ).first()
            if not user_profile:
                return Response(
                    {'message': 'Такой номер не зарегистрирован'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(
                {'invite_code': user_profile.invite_code},
                status=status.HTTP_200_OK
            )

        # Если номер телефона не предоставлен, отобразить HTML-шаблон
        return render(request, 'profile.html')


class ReferralListView(APIView):

    @swagger_auto_schema(
        operation_description='Выводит всех рефералов, активировавших ваш '
                              'инвайт-код.',
        responses={200: ReferralSerializer}
    )
    def get(self, request, *args, **kwargs):
        phone_number = request.GET.get('phone_number')

        if not phone_number:
            return render(request, 'referrals.html')

        user_profile = UserProfile.objects.filter(
            phone_number=phone_number
        ).first()
        if not user_profile:
            return Response(
                {'message': 'Такой номер не зарегистрирован'},
                status=status.HTTP_404_NOT_FOUND
            )
        referrals = UserProfile.objects.filter(
            activated_invite_code=user_profile
        )
        serializer = ReferralSerializer(referrals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
