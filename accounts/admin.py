from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group, Permission

# ── MIXIN: User-Friendly Permissions ──────────────────────────────────────────

class UserFriendlyPermissionMixin:
    """Provides filtered, readable permission management for Users and Groups."""
    
    # Hide technical system apps to focus on business logic
    SYSTEM_APPS = ['admin', 'contenttypes', 'sessions', 'messages', 'staticfiles', 'auth']

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name in ["permissions", "user_permissions"]:
            # Filter the queryset to exclude internal system apps
            kwargs["queryset"] = Permission.objects.exclude(content_type__app_label__in=self.SYSTEM_APPS)
            # Use standard widget so filter_horizontal works correctly with our CSS
            return super().formfield_for_manytomany(db_field, request, **kwargs)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

# ── CUSTOM ADMINS ──────────────────────────────────────────────────────────────

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(UserFriendlyPermissionMixin, BaseUserAdmin):
    """
    Refined User Management with high-readability permissions.
    """
    filter_horizontal = ('groups', 'user_permissions')

    class Media:
        css = {
            'all': ('admin/css/admin_offer.css',)
        }
    
    # We remove the get_form override that was adding select2 since we have a custom widget now
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'groups' in form.base_fields:
            form.base_fields['groups'].widget.attrs['class'] = 'select2'
        return form

admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(UserFriendlyPermissionMixin, BaseGroupAdmin):
    """
    Refined Group Management with filtered permissions.
    """
    filter_horizontal = ('permissions',)

    class Media:
        css = {
            'all': ('admin/css/admin_offer.css',)
        }
