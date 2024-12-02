# manager_app/admin.py
from django.contrib import admin
from .models import Branch, Manager

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'branch', 'phone_number')
    list_filter = ('branch',)
    search_fields = ('user__username', 'phone_number')
