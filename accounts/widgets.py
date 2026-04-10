
from django import forms
from django.contrib.auth.models import Permission
from django.utils.safestring import mark_safe
from itertools import groupby

class PermissionMenuWidget(forms.SelectMultiple):
    """
    A premium, menu-based widget for managing permissions.
    Groups permissions by app and provides a clean toggle interface.
    """
    template_name = 'admin/accounts/permission_menu.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        
        # Get all permissions in the current queryset
        if hasattr(self.choices, 'queryset'):
            queryset = self.choices.queryset.select_related('content_type').order_by('content_type__app_label', 'content_type__model', 'name')
        else:
            # Fallback for unexpected choice structures
            queryset = Permission.objects.all().select_related('content_type').order_by('content_type__app_label', 'content_type__model', 'name')
        
        # Grouping logic
        grouped = {}
        for app, app_perms in groupby(queryset, lambda p: p.content_type.app_label):
            app_name = app.title().replace('_', ' ')
            grouped[app_name] = []
            
            # Sub-group by model if needed, but for "Minimalist" view, we can just list them
            # or sub-group by modern "Module" names
            for p in app_perms:
                # Simplify name: "Can add product" -> "Add"
                action = "View"
                if "add" in p.codename: action = "Add"
                elif "change" in p.codename: action = "Edit"
                elif "delete" in p.codename: action = "Delete"
                
                model_name = p.content_type.model_name.title().replace('_', ' ')
                
                grouped[app_name].append({
                    'id': p.id,
                    'action': action,
                    'model': model_name,
                    'name': p.name,
                    'selected': str(p.id) in [str(v) for v in (value or [])]
                })
        
        context['grouped_permissions'] = grouped
        return context

    class Media:
        css = {
            'all': ('admin/css/permission_menu.css',)
        }
        js = ('admin/js/permission_menu.js',)
