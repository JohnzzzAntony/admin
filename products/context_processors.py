from .models import Category

def categories(request):
    try:
        return {
            'categories': Category.objects.filter(parent__isnull=True, is_active=True).order_by('homepage_order', 'name')
        }
    except Exception:
        return {'categories': []}
