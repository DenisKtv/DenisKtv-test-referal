import random
import string

from django.db import models


class UserProfile(models.Model):
    phone_number = models.CharField(
        'Номер телефона',
        unique=True,
        max_length=20,
        null=False
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
    entered_invite_code = models.CharField(
        'Введенный инвайт-код',
        max_length=6,
        null=True,
        blank=True
    )

    def generate_invite_code(self):
        while True:
            code = ''.join(
                random.choices(string.ascii_letters + string.digits, k=6)
            )
            if not UserProfile.objects.filter(invite_code=code).exists():
                self.invite_code = code
                break

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.phone_number
