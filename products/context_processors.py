from .models import Category, Wishlist, Brand

def categories(request):
    try:
        return {
            'categories': Category.objects.filter(parent__isnull=True, is_active=True).order_by('homepage_order', 'name'),
            'all_brands_count': Brand.objects.filter(is_active=True).count()
        }
    except Exception:
        return {'categories': [], 'all_brands_count': 0}

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
