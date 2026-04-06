from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter(name='split')
def split(value, key):
    return value.split(key)

@register.filter(name='get_attr')
def get_attr(obj, attr):
    return getattr(obj, attr, None)
