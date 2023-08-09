from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'phone_number',
        'invite_code',
        'activated_invite_code'
    )
    ordering = ('id',)
