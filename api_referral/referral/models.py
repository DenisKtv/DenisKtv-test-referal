import random
import re
import string
from django.db import models
from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    phone_number = models.CharField(
        'Номер телефона',
        max_length=15,
        unique=True
    )
    nickname = models.CharField(
        'Ник',
        max_length=30,
        unique=True
    )
    invite_code = models.CharField(
        'Инвайт-код',
        max_length=6,
        unique=True,
        blank=True
    )
    activated_invite_code = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referrals'
    )

    def generate_invite_code(self):
        self.invite_code = ''.join(
            random.choices(string.ascii_letters + string.digits, k=6)
        )

    def clean(self):
        forbidden_characters = r'[!"№%:,.;()[]{}@#$%^&*?/\\|]'
        if re.search(forbidden_characters, self.nickname):
            raise ValidationError('Никнейм содержит недопустимые символы.')

    def __str__(self):
        return self.nickname
