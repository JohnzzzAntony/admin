import re
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q

# ── HELPER: User-Friendly Permissions ──────────────────────────────────────────

def get_readable_permission_label(perm):
    """Refines standard Django permission labels into professional, logical names."""
    # Pattern: [App] | [Model] | [Action] -> [App]: [Action] [Model]
    # Example: products | Category | Can add Category -> Products: Add Category
    content_type = perm.content_type
    app_label = content_type.app_label.title()
    name = perm.name.replace('Can add ', 'Add ') \
                    .replace('Can change ', 'Change ') \
                    .replace('Can delete ', 'Delete ') \
                    .replace('Can view ', 'View ')
    
    # Hide the model repetition if it exists in the name
    model_name = content_type.model_name.title()
    # If name ends with the model name, we keep it as is or refine
    return f"{app_label}: {name}"

# List of internal app labels we want to hide to reduce clutter
SYSTEM_APPS = ['admin', 'contenttypes', 'sessions', 'messages', 'staticfiles']

# Overriding ChoiceField to use our readable labels
class UserFriendlyPermissionField(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name in ["permissions", "user_permissions"]:
            # Filter out system apps
            kwargs["queryset"] = Permission.objects.exclude(content_type__app_label__in=SYSTEM_APPS)
            field = super().formfield_for_manytomany(db_field, request, **kwargs)
            # Apply readable labels
            field.label_from_instance = get_readable_permission_label
            return field
        return super().formfield_for_manytomany(db_field, request, **kwargs)

# ── CUSTOM ADMINS ──────────────────────────────────────────────────────────────

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin, UserFriendlyPermissionField):
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
class GroupAdmin(UserFriendlyPermissionField):
    """
    Refined Group Management with filtered permissions.
    """
    filter_horizontal = ()
    list_display = ('name',)
    search_fields = ('name',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'permissions' in form.base_fields:
            form.base_fields['permissions'].widget.attrs['class'] = 'select2'
        return form
