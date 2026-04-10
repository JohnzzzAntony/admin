import re
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q

# ── MIXIN: User-Friendly Permissions ──────────────────────────────────────────

class UserFriendlyPermissionMixin:
    """Provides filtered, readable permission management for Users and Groups."""
    
    # Hide technical system apps to focus on business logic
    SYSTEM_APPS = ['admin', 'contenttypes', 'sessions', 'messages', 'staticfiles', 'auth']

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name in ["permissions", "user_permissions"]:
            # Filter the queryset to exclude internal system apps
            kwargs["queryset"] = Permission.objects.exclude(content_type__app_label__in=self.SYSTEM_APPS)
            field = super().formfield_for_manytomany(db_field, request, **kwargs)
            
            # Apply refined readable labels
            def get_readable_label(perm):
                app_label = perm.content_type.app_label.title()
                # Clean up the action name
                name = perm.name.replace('Can add ', 'Add ') \
                                .replace('Can change ', 'Change ') \
                                .replace('Can delete ', 'Delete ') \
                                .replace('Can view ', 'View ')
                return f"{app_label}: {name}"
            
            field.label_from_instance = get_readable_label
            return field
        return super().formfield_for_manytomany(db_field, request, **kwargs)

# ── CUSTOM ADMINS ──────────────────────────────────────────────────────────────

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(UserFriendlyPermissionMixin, BaseUserAdmin):
    """
    Refined User Management with high-readability permissions.
    """
    filter_horizontal = ()
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'user_permissions' in form.base_fields:
            form.base_fields['user_permissions'].widget.attrs['class'] = 'select2'
        if 'groups' in form.base_fields:
            form.base_fields['groups'].widget.attrs['class'] = 'select2'
        return form

admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(UserFriendlyPermissionMixin, BaseGroupAdmin):
    """
    Refined Group Management with filtered permissions.
    """
    filter_horizontal = ()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'permissions' in form.base_fields:
            form.base_fields['permissions'].widget.attrs['class'] = 'select2'
        return form
