# authentication/admin.py
from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'role', 'email')
    list_filter = ('role',)
    search_fields = ('username', 'email')
