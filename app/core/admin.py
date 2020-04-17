from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from core import models


class CustomUserAdmin(UserAdmin):

    def activate_accounts(self, request, queryset):
        """Activates selected accounts"""
        queryset.update(is_active=True)

    def deactivate_accounts(self, request, queryset):
        """Deactivates selected accounts"""
        queryset.update(is_active=False)

    def add_staff_permission(self, request, queryset):
        """Adds staff permission to selected accounts"""
        queryset.update(is_staff=True)

    def remove_staff_permission(self, request, queryset):
        """Adds staff permission to selected accounts"""
        queryset.update(is_staff=False)

    activate_accounts.short_description = 'Activate accounts'
    deactivate_accounts.short_description = 'Deactivate accounts'
    add_staff_permission.short_descriptin = 'Add Staff permission'
    remove_staff_permission.short_descriptin = 'Remove Staff permission'

    ordering = ['id']
    list_display = [
        'email', 'username', 'is_superuser', 'is_staff', 'is_active',
    ]
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    search_fields = ['email', 'username', ]
    actions = [
        activate_accounts,
        deactivate_accounts,
        add_staff_permission,
        remove_staff_permission
    ]
    fieldsets = (
        (
            None,
            {'fields': ('email', 'username', 'password')}
        ),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser',)}
        ),
        (
            _('Important Dates'),
            {'classes': ('collapse',), 'fields': ('last_login', )}
        )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, CustomUserAdmin)
