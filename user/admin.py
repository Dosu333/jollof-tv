from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.apps import apps
from django.utils.translation import gettext as _
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name']
    search_fields = ('id', 'email', 'first_name', 'lastname', 'phone', 'country', 'state', 'city')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {
            'fields': ('first_name', 'last_name', 'phone', 'country', 'state', 'city')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'verified')}
        ),
        (_('Important Info'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'verified', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)