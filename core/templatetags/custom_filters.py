from django import template
from core.models import SiteSettings
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.simple_tag
def get_site_settings():
    return SiteSettings.objects.first()

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return float(Decimal(str(value)) * Decimal(str(arg)))
    except (ValueError, TypeError, InvalidOperation):
        return 0

@register.filter(name='split')
def split(value, key):
    return value.split(key)

@register.filter(name='get_attr')
def get_attr(obj, attr):
    return getattr(obj, attr, None)
