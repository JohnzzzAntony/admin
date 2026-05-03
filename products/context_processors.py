from django.core.cache import cache
from .models import Category, Wishlist, Brand


def categories(request):
    """
    Global mega-menu data: cached for 5 minutes to avoid repeated DB hits on
    every page load. Invalidate manually when categories/brands are updated
    (e.g. via admin save signal).
    """
    cache_key = 'global_nav_categories_v1'
    data = cache.get(cache_key)
    if data is None:
        try:
            cats = list(
                Category.objects.filter(parent__isnull=True, is_active=True)
                .prefetch_related('subcategories')
                .order_by('homepage_order', 'name')
            )
            brands = list(Brand.objects.filter(is_active=True).order_by('name'))
            data = {
                'categories': cats,
                'all_brands': brands,
                'all_brands_count': len(brands),  # avoid extra COUNT(*) query
            }
            cache.set(cache_key, data, 300)  # Cache 5 minutes
        except Exception:
            data = {'categories': [], 'all_brands': [], 'all_brands_count': 0}
    return data


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
