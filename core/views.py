from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.db import models
from products.models import Category, Product, Collection, Brand
from sliders.models import HeroSlider, PromoBanner
from pages.models import AboutUs, MissionVision, Service, Counter, WhyUsCard, Partner, GalleryItem
from .models import Testimonial, Client, SocialPost, StoreLocation

def home(request):
    """Homepage aggregation view."""
    sliders = HeroSlider.objects.all().order_by('order')
    
    # Homepage Interleaving Logic
    # Homepage sections logic
    homepage_sections_raw = Category.objects.filter(show_on_homepage=True)
    
    # Categories for the circular slider (Top)
    categories_circles = homepage_sections_raw
    if not categories_circles.exists():
        categories_circles = Category.objects.filter(parent__isnull=True)[:10]
    
    # Merge and Sort
    homepage_sections = []
    for cat in homepage_sections_raw:
        # Aggregated products for this category and all its children
        all_cat_ids = [c.id for c in cat.get_all_children(include_self=True)]
        cat_products = Product.objects.filter(
            category_id__in=all_cat_ids,
            is_active=True,
            quantity__gt=0
        ).distinct().order_by('-id')[:8] # Limit to 8 products per section
        
        # Attach aggregated products to the category object for template access
        cat.aggregated_products = cat_products
        
        if cat_products.exists():
            homepage_sections.append({'type': 'category', 'data': cat, 'order': cat.homepage_order})
    
    banners = PromoBanner.objects.filter(is_active=True).prefetch_related('items')
    for banner in banners:
        homepage_sections.append({'type': 'banner', 'data': banner, 'order': banner.homepage_order})
    
    # Sort everything by the order value
    homepage_sections.sort(key=lambda x: x['order'])

    about_us = AboutUs.objects.first()
    
    # Batch Mission/Vision queries to reduce one round-trip
    mv_sections = MissionVision.objects.filter(section_type__in=['mission', 'vision'])
    mission = next((mv for mv in mv_sections if mv.section_type == 'mission'), None)
    vision = next((mv for mv in mv_sections if mv.section_type == 'vision'), None)
    
    services = Service.objects.all()
    counters = Counter.objects.all()
    why_us = WhyUsCard.objects.all()
    partners = Partner.objects.all().order_by('order')
    gallery = GalleryItem.objects.all().order_by('order')[:8]
    
    testimonials = Testimonial.objects.all().order_by('order')
    public_clients = Client.objects.filter(category='Public').order_by('order')
    private_clients = Client.objects.filter(category='Private').order_by('order')
    social_posts = SocialPost.objects.all().order_by('order')[:6]
    
    # Optimized latest_products
    latest_products = Product.objects.filter(
        quantity__gt=0
    ).select_related('category').prefetch_related('offers').order_by('-id')[:4]

    # Fetch Products with active offers (either via Offer model or manual sale_price)
    now = timezone.now()
    active_offers_products = Product.objects.filter(
        is_active=True,
        quantity__gt=0,
    ).filter(
        models.Q(offers__start_date__lte=now, offers__end_date__gte=now) |
        models.Q(sale_price__isnull=False, sale_price__lt=models.F('regular_price'))
    ).distinct().select_related('category').prefetch_related('offers', 'images')

    # Homepage Collections: Filter active ones and prefetch related Products.
    collections = Collection.objects.all().prefetch_related(
        'products', 
        'products__category',
        'products__offers'
    )

    brands = Brand.objects.filter(show_on_homepage=True, is_active=True)

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
        'homepage_sections': homepage_sections,
        'brands': brands,
    }
    return render(request, 'index.html', context)

def about_us_view(request):
    """Specific About Us page."""
    about_us = AboutUs.objects.first()
    mission = MissionVision.objects.filter(section_type='mission').first()
    vision = MissionVision.objects.filter(section_type='vision').first()
    return render(request, 'pages/about.html', {
        'about_us': about_us,
        'mission': mission,
        'vision': vision
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
    """Store Locations page with city filtering."""
    stores = StoreLocation.objects.all().order_by('order', 'name')
    # Get unique cities for filter tabs
    cities = StoreLocation.objects.all().values_list('city', flat=True).distinct().order_by('city')
    
    return render(request, 'pages/stores.html', {
        'stores': stores,
        'cities': cities
    })
def health_check(request):
    """Simple health check endpoint for monitoring."""
    return JsonResponse({'status': 'healthy', 'timestamp': timezone.now().isoformat()})
