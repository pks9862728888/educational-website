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
        'is_student', 'is_teacher'
    ]
    list_filter = ('is_superuser', 'is_staff', 'is_active',
                   'is_teacher', 'is_student')
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
            {'fields': ('is_active', 'is_staff', 'is_superuser',
                        'is_student', 'is_teacher')}
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


class CustomClassroomAdmin(admin.ModelAdmin):
    model = models.Classroom
    list_display = ['name', 'get_user']
    list_filter = ['user__email', ]

    def get_user(self, obj):
        return obj.user.email
    get_user.admin_order_field = 'name'  # Allows column order sorting
    get_user.short_description = 'Email of user'  # Renames column head


class CustomSubjectAdmin(admin.ModelAdmin):
    model = models.Subject
    list_display = ['name', 'get_classroom', 'get_user']
    list_filter = ['user__email', 'classroom__name']

    def get_user(self, obj):
        return obj.user.email
    get_user.admin_order_field = 'name'  # Allows column order sorting
    get_user.short_description = 'Email of user'  # Renames column head

    def get_classroom(self, obj):
        return obj.classroom.name
    get_classroom.short_description = 'Classroom name'  # Renames column head


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.Classroom, CustomClassroomAdmin)
admin.site.register(models.Subject, CustomSubjectAdmin)
