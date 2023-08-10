from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'phone_number',
        'invite_code',
        'entered_invite_code',
        'activated_invite_code'
    )
    ordering = ('id',)
    search_fields = ('phone_number', 'invite_code',)
    list_filter = ('activated_invite_code',)
