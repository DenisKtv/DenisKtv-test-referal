import time
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from .models import UserProfile
import random
from .serializers import SignUpSerializer, SignInSerializer


class VerificationView(APIView):
    def generate_verification_code(self, phone_number):
        verification_code = random.randint(1000, 9999)
        cache.set(phone_number, verification_code, timeout=90)
        time.sleep(2)
        return verification_code

    def check_verification_code(self, phone_number, verification_code):
        cached_code = cache.get(phone_number)
        return cached_code == int(verification_code)

    def check_phone_number_existence(self, phone_number, should_exist):
        exists = UserProfile.objects.filter(phone_number=phone_number).exists()
        return exists if should_exist else not exists


class SignUpView(VerificationView):
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        phone_number = request.data.get('phone_number')
        verification_code = request.data.get('verification_code')
        username = request.data.get('username')

        if not self.check_phone_number_existence(phone_number, False):
            return Response(
                {"message": "Телефон уже зарегистрирован"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if UserProfile.objects.filter(username=username).exists():
            return Response(
                {"message": "Логин уже зарегистрирован"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if verification_code is None:
            verification_code = self.generate_verification_code(phone_number)
            return Response(
                {"verification_code": verification_code},
                status=status.HTTP_200_OK
            )

        if not self.check_verification_code(phone_number, verification_code):
            return Response(
                {"message": "Код верификации неверен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_profile = UserProfile(
            phone_number=phone_number, username=username
        )
        user_profile.generate_invite_code()
        user_profile.save()

        return Response(
            {"message": "Регистрация успешно пройдена"},
            status=status.HTTP_201_CREATED
        )


class LogInView(VerificationView):
    serializer_class = SignInSerializer

    def post(self, request):
        phone_number = request.data.get('phone_number')
        verification_code = request.data.get('verification_code')

        if not self.check_phone_number_existence(phone_number, True):
            return Response(
                {"message": "Телефон не зарегистрирован"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if verification_code is None:
            verification_code = self.generate_verification_code(phone_number)
            return Response(
                {"verification_code": verification_code},
                status=status.HTTP_200_OK
            )

        if not self.check_verification_code(phone_number, verification_code):
            return Response(
                {"message": "Код верификации неверен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Здесь можно создать и вернуть токен, если это необходимо
        # ...

        return Response(
            {"message": "Авторизация успешна"},
            status=status.HTTP_200_OK
        )
