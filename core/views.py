from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
from django.core.paginator import Paginator
from django.utils import timezone
from .models import SiteSettings, Testimonial, Client, SocialPost, StoreLocation
from django.db import models
from products.models import Category, Product, Collection, Brand, Offer
from sliders.models import HeroSlider, PromoBanner
from pages.models import AboutUs, MissionVision, Service, Counter, WhyUsCard, Partner, GalleryItem
from .models import Testimonial, Client, SocialPost, StoreLocation

def home(request):
    """Homepage aggregation view — anonymous requests are cached for 5 minutes."""
    # Only cache for anonymous users (authenticated users may have personalised data)
    cache_key = 'homepage_context_v2'
    if not request.user.is_authenticated:
        context = cache.get(cache_key)
        if context is not None:
            return render(request, 'index.html', context)

    sliders = list(HeroSlider.objects.filter(is_active=True).order_by('order'))

    # Homepage sections logic
    homepage_sections_raw = list(
        Category.objects.filter(show_on_homepage=True, is_active=True)
        .prefetch_related('subcategories')
    )

    # Categories for the circular slider (Top) — reuse the already-fetched list
    categories_circles = homepage_sections_raw or list(
        Category.objects.filter(parent__isnull=True, is_active=True)[:10]
    )

    # Pre-fetch all active category relations once for efficient descendant lookup
    all_cats_lookup = list(Category.objects.filter(is_active=True).values('id', 'parent_id'))

    # ─── Homepage Interleaving Logic ──────────────────────────────────────────
    category_sections = []
    for cat in homepage_sections_raw:
        all_cat_ids = cat.get_descendant_ids(include_self=True, all_cats_prefetched=all_cats_lookup)
        # Evaluate the queryset immediately (list) to avoid extra .exists() COUNT query
        cat_products = list(
            Product.objects.filter(
                category_id__in=all_cat_ids,
                is_active=True,
                quantity__gt=0
            ).select_related('category', 'brand').prefetch_related('offers', 'images')
            .distinct().order_by('-id')[:8]
        )
        cat.aggregated_products = cat_products
        if cat_products:  # len() check — no extra COUNT query
            category_sections.append({'type': 'category', 'data': cat, 'order': cat.homepage_order})

    category_sections.sort(key=lambda x: x['order'])

    banners = list(PromoBanner.objects.filter(is_active=True).prefetch_related('items'))
    banner_sections = [
        {'type': 'banner', 'data': b, 'order': b.homepage_order} for b in banners
    ]
    banner_sections.sort(key=lambda x: x['order'])

    homepage_sections = sorted(category_sections + banner_sections, key=lambda x: x.get('order', 0))
    cat_display_count = 1
    for section in homepage_sections:
        if section['type'] == 'category':
            section['display_index'] = cat_display_count
            cat_display_count += 1

    about_us = AboutUs.objects.filter(is_active=True).first()

    # Single query for both mission and vision
    mv_sections = list(MissionVision.objects.filter(section_type__in=['mission', 'vision'], is_active=True))
    mission = next((mv for mv in mv_sections if mv.section_type == 'mission'), None)
    vision = next((mv for mv in mv_sections if mv.section_type == 'vision'), None)

    services  = list(Service.objects.filter(is_active=True).order_by('order'))
    counters  = list(Counter.objects.filter(is_active=True).order_by('order'))
    why_us    = list(WhyUsCard.objects.filter(is_active=True).order_by('order'))
    partners  = list(Partner.objects.filter(is_active=True).order_by('order'))
    gallery   = list(GalleryItem.objects.filter(is_active=True).order_by('order')[:8])
    testimonials   = list(Testimonial.objects.filter(is_active=True).order_by('order'))
    public_clients = list(Client.objects.filter(category='Public', is_active=True).order_by('order'))
    private_clients= list(Client.objects.filter(category='Private', is_active=True).order_by('order'))
    social_posts   = list(SocialPost.objects.all().order_by('order')[:6])

    latest_products = list(
        Product.objects.filter(quantity__gt=0, is_active=True)
        .select_related('category', 'brand').prefetch_related('offers', 'images')
        .order_by('-id')[:8]
    )

    now = timezone.now()
    active_offers_products = list(
        Product.objects.filter(is_active=True, quantity__gt=0).filter(
            models.Q(offers__start_date__lte=now, offers__end_date__gte=now) |
            models.Q(sale_price__isnull=False, sale_price__lt=models.F('regular_price'))
        ).distinct().select_related('category', 'brand').prefetch_related('offers', 'images')
    )

    # Evaluate featured products as a list first to avoid double DB hit
    featured_products = list(
        Product.objects.filter(is_featured=True, is_active=True, quantity__gt=0)
        .select_related('category', 'brand').prefetch_related('offers', 'images')
        .order_by('-id')[:8]
    )
    if not featured_products:  # use already-fetched list — no extra COUNT query
        featured_products = latest_products

    all_active_offers = list(
        Offer.objects.filter(start_date__lte=now, end_date__gte=now)
        .prefetch_related('products', 'categories', 'brands')
    )

    def attach_price_info(product_list):
        for p in product_list:
            p.price_info = p.get_best_price_info(prefetched_offers=all_active_offers)

    attach_price_info(latest_products)
    attach_price_info(featured_products)
    attach_price_info(active_offers_products)
    for section in category_sections:
        attach_price_info(section['data'].aggregated_products)

    collections = list(
        Collection.objects.filter(is_active=True).prefetch_related(
            'products', 'products__category', 'products__brand',
            'products__offers', 'products__images'
        )
    )
    for col in collections:
        attach_price_info(list(col.products.all()))

    brands = list(Brand.objects.filter(show_on_homepage=True, is_active=True).order_by('order'))

    context = {
        'sliders': sliders,
        'categories': categories_circles,
        'collections': collections,
        'active_offers_products': active_offers_products,
        'about_us': about_us,
        'mission_vision': [mv for mv in [mission, vision] if mv],
        'services': services,
        'counters': counters,
        'why_us': why_us,
        'partners': partners,
        'gallery': gallery,
        'testimonials': testimonials,
        'public_clients': public_clients,
        'private_clients': private_clients,
        'social_posts': social_posts,
        'latest_products': latest_products,
        'featured_products': featured_products,
        'promo_banners': banners,
        'homepage_sections': homepage_sections,
        'brands': brands,
    }

    # Store in cache for anonymous users (5 minutes)
    if not request.user.is_authenticated:
        cache.set(cache_key, context, 300)

    return render(request, 'index.html', context)

def about_us_view(request):
    """Specific About Us page — single query for mission+vision."""
    about_us = AboutUs.objects.first()
    # One query for both instead of two separate .filter().first() calls
    mv_qs = list(MissionVision.objects.filter(section_type__in=['mission', 'vision']))
    mission = next((mv for mv in mv_qs if mv.section_type == 'mission'), None)
    vision  = next((mv for mv in mv_qs if mv.section_type == 'vision'), None)
    counters = list(Counter.objects.filter(is_active=True).order_by('order'))
    return render(request, 'pages/about.html', {
        'about_us': about_us,
        'mission': mission,
        'vision': vision,
        'counters': counters
    })

def services_view(request):
    """Specific Services page."""
    services = Service.objects.all().order_by('order')
    return render(request, 'pages/services.html', {'services': services})

def gallery_view(request):
    """Specific Gallery page."""
    gallery = GalleryItem.objects.all().order_by('order')
    return render(request, 'pages/gallery.html', {'gallery': gallery})

def store_locations_view(request):
    """Store Locations page with server-side city filtering and pagination."""
    selected_city = request.GET.get('city', 'all')
    stores_qs = StoreLocation.objects.all().order_by('order', 'name')
    
    if selected_city != 'all':
        stores_qs = stores_qs.filter(city=selected_city)
    
    paginator = Paginator(stores_qs, 9) # 9 stores per page (3x3 grid)
    page_number = request.GET.get('page')
    stores = paginator.get_page(page_number)
    
    cities = StoreLocation.objects.all().values_list('city', flat=True).distinct().order_by('city')
    
    return render(request, 'pages/stores.html', {
        'stores': stores,
        'cities': cities,
        'selected_city': selected_city
    })
def health_check(request):
    """Simple health check endpoint for monitoring."""
    return JsonResponse({'status': 'healthy', 'timestamp': timezone.now().isoformat()})
def robots_txt_view(request):
    """Serve dynamic robots.txt — cached for 24h to avoid DB hit on every crawler request."""
    cache_key = 'robots_txt_v1'
    content = cache.get(cache_key)
    if content is None:
        site = SiteSettings.objects.first()
        content = (site.robots_txt if site and site.robots_txt
                   else "User-agent: *\nDisallow: /admin/\nDisallow: /checkout/\nAllow: /")
        cache.set(cache_key, content, 86400)  # 24 hours
    return HttpResponse(content, content_type="text/plain")
