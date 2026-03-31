from django.shortcuts import render
from django.utils import timezone
from products.models import Category, Product, Collection, ProductSKU
from sliders.models import HeroSlider
from pages.models import AboutUs, MissionVision, Service, Counter, WhyUsCard, Partner, GalleryItem
from .models import Testimonial, Client, SocialPost

def home(request):
    """Homepage aggregation view."""
    sliders = HeroSlider.objects.filter(is_active=True).order_by('order')
    # Homepage categories: Filtered by 'Show on Homepage' toggle and custom sort order.
    categories = Category.objects.filter(show_on_homepage=True).order_by('homepage_order')
    about_us = AboutUs.objects.first()
    
    mission = MissionVision.objects.filter(section_type='mission').first()
    vision = MissionVision.objects.filter(section_type='vision').first()
    
    services = Service.objects.all()
    counters = Counter.objects.all()
    why_us = WhyUsCard.objects.all()
    partners = Partner.objects.all().order_by('order')
    gallery = GalleryItem.objects.all().order_by('order')[:8]
    
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')
    public_clients = Client.objects.filter(category='Public', is_active=True).order_by('order')
    private_clients = Client.objects.filter(category='Private', is_active=True).order_by('order')
    social_posts = SocialPost.objects.all().order_by('order')[:6]
    
    # Homepage should only show in-stock items
    latest_products = Product.objects.filter(
        is_active=True,
        skus__quantity__gt=0,
        skus__shipping_status='available'
    ).distinct().order_by('-id')[:4]

    # Fetch SKUs with active offers (Part of fallback/offers logic)
    now = timezone.now()
    active_offers_skus = ProductSKU.objects.filter(
        offers__is_active=True,
        offers__start_date__lte=now,
        offers__end_date__gte=now,
        quantity__gt=0
    ).distinct().prefetch_related('product', 'product__category')

    # Homepage Collections: Filter active ones and prefetch related SKUs for efficient rendering.
    collections = Collection.objects.filter(is_active=True).prefetch_related('skus__product')

    context = {
        'sliders': sliders,
        'categories': categories,
        'collections': collections,
        'active_offers_skus': active_offers_skus,
        'about_us': about_us,
        'mission': mission,
        'vision': vision,
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
