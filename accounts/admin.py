from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group

# Unregister the default User admin
admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom UserAdmin that replaces the clunky horizontal filter boxes 
    with a modern, searchable dropdown for Permissions and Groups.
    """
    # Using autocomplete_fields for a much cleaner "Searchable Dropdown" experience
    # Note: For these to work perfectly, we also register a simple GroupAdmin if needed.
    filter_horizontal = () # Disable the old big boxes
    
    # We will use select2 (via jazzmin/django defaults) for better visibility
    # This makes the permission selection a single row that expands on click
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'user_permissions' in form.base_fields:
            form.base_fields['user_permissions'].widget.attrs['class'] = 'select2'
        if 'groups' in form.base_fields:
            form.base_fields['groups'].widget.attrs['class'] = 'select2'
        return form

# Also optimize Group admin if needed
admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ()
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'permissions' in form.base_fields:
            form.base_fields['permissions'].widget.attrs['class'] = 'select2'
        return form
