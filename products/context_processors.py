from .models import Category, Wishlist, Brand

def categories(request):
    try:
        # Optimizing fetch for the mega-menu to prevent N+1 queries
        cats = Category.objects.filter(parent__isnull=True, is_active=True)\
            .prefetch_related('subcategories')\
            .order_by('homepage_order', 'name')
        
        brands = Brand.objects.filter(is_active=True).order_by('name')
        
        return {
            'categories': cats,
            'all_brands': brands,
            'all_brands_count': brands.count()
        }
    except Exception:
        return {'categories': [], 'all_brands': [], 'all_brands_count': 0}

def wishlist_data(request):
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        wish_ids = list(Wishlist.objects.filter(user=user).values_list('product_id', flat=True))
        count = len(wish_ids)
    else:
        count = 0
        wish_ids = []
    return {
        'wishlist_count': count,
        'wishlist_ids': wish_ids
    }
