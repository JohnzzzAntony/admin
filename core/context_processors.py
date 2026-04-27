from django.utils import timezone
from django.db.models import Q, Sum
from .models import SiteSettings, AnnouncementBar
from .design_models import DesignSettings
from products.models import Product
from orders.models import CustomerOrder
from contact.models import ContactFormSubmission
from blog.models import Post

from django.core.cache import cache

def site_settings(request):
    """
    Cached site-wide settings and announcements.
    """
    # Try to get everything from cache first
    cache_key = 'site_wide_settings_v1'
    data = cache.get(cache_key)
    
    if data is None:
        try:
            settings = SiteSettings.objects.first()
            now = timezone.now()
            announcements = list(AnnouncementBar.objects.filter(is_active=True).filter(
                Q(start_date__isnull=True) | Q(start_date__lte=now)
            ).filter(
                Q(end_date__isnull=True) | Q(end_date__gte=now)
            ).order_by('id'))
            
            design = DesignSettings.objects.first()
            latest_posts = list(Post.objects.filter(is_published=True).order_by('-created_at')[:3])
            
            data = {
                'site_settings': settings,
                'design_settings': design,
                'announcement_bar_list': announcements,
                'latest_blog_posts': latest_posts,
            }
            # Cache for 1 hour
            cache.set(cache_key, data, 3600)
        except Exception:
            return {
                'site_settings': None,
                'design_settings': None,
                'announcement_bar_list': [],
                'latest_blog_posts': [],
            }
            
    return data

def page_heroes(request):
    from pages.models import PageHero
    try:
        # Get existing heroes
        db_heroes = {hero.page: hero for hero in PageHero.objects.filter(is_active=True)}
        
        # Ensure all choices have an object (even if unsaved)
        heroes = {}
        for choice_key, choice_label in PageHero.PAGE_CHOICES:
            if choice_key in db_heroes:
                heroes[choice_key] = db_heroes[choice_key]
            else:
                # Return an unsaved instance with the page set
                # This allows templates to call .display_title etc.
                heroes[choice_key] = PageHero(page=choice_key, is_active=True)
                
    except Exception:
        heroes = {}
        
    return {
        'page_heroes': heroes,
    }


def admin_dashboard(request):
    """Provides key metrics for the admin dashboard summary."""
    if not request.path.startswith('/admin/'):
        return {}
    
    try:
        total_orders = CustomerOrder.objects.count()
        total_revenue = CustomerOrder.objects.filter(payment_status='paid').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_products = Product.objects.count()
        new_messages = ContactFormSubmission.objects.filter(is_read=False).count()
        
        return {
            'dashboard_summary': {
                'orders': total_orders,
                'revenue': f"{total_revenue:,.2f}",
                'products': total_products,
                'messages': new_messages
            }
        }
    except Exception:
        return {}
