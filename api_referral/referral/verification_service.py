from django.core.cache import cache
import random


class VerificationService:
    @staticmethod
    def generate_verification_code(phone_number):
        verification_code = random.randint(1000, 9999)
        cache.set(phone_number, verification_code, timeout=90)
        return verification_code

    @staticmethod
    def check_verification_code(phone_number, verification_code):
        cached_code = cache.get(phone_number)
        return cached_code == verification_code
