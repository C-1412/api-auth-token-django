from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_admin', 'is_superadmin', 'created', 'modified')
    list_filter = ('is_active', 'is_admin', 'is_superadmin', 'created')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superadmin', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created', 'modified')}),
    )
    readonly_fields = ('created', 'modified')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_admin', 'is_superadmin'),
        }),
    )

# Registrar Group y Permission en el admin si no están registrados
admin.site.unregister(Group)
admin.site.register(Group)
admin.site.register(Permission)