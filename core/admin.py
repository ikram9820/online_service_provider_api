from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from service_provider.admin import UserLocationInline


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserLocationInline]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name','contact'),
        }),
    )

