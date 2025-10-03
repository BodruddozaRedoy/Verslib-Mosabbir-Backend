from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from .models import User  # যদি আপনার কাস্টম ইউজার মডেল User নামে থাকে

# Custom UserAdmin
class UserAdmin(BaseUserAdmin, ModelAdmin):
    model = User
    list_display = ('email', 'username', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password','bio','image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    autocomplete_fields = ('groups',)

# Register the custom UserAdmin
admin.site.register(User, UserAdmin)

