from .models import Category, Wishlist

def categories(request):
    try:
        return {
            'categories': Category.objects.filter(parent__isnull=True, is_active=True).order_by('homepage_order', 'name')
        }
    except Exception:
        return {'categories': []}

def wishlist_data(request):
    if request.user.is_authenticated:
        count = Wishlist.objects.filter(user=request.user).count()
        wish_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
    else:
        count = 0
        wish_ids = []
    return {
        'wishlist_count': count,
        'wishlist_ids': wish_ids
    }
