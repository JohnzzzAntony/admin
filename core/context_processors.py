from django.utils import timezone
from django.db.models import Q
from .models import SiteSettings, AnnouncementBar
from .design_models import DesignSettings

def site_settings(request):
    now = timezone.now()
    
    try:
        settings = SiteSettings.objects.first()
        now = timezone.now()
        announcements = AnnouncementBar.objects.filter(
            Q(start_date__isnull=True) | Q(start_date__lte=now)
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=now)
        ).order_by('id')
    except Exception:
        settings = None
        announcements = []
        
    try:
        design = DesignSettings.objects.first()
    except:
        design = None
        
    return {
        'site_settings': settings,
        'design_settings': design,
        'announcement_bar_list': announcements,
    }

def page_heroes(request):
    from pages.models import PageHero
    try:
        heroes = {hero.page: hero for hero in PageHero.objects.all()}
    except:
        heroes = {}
    return {
        'page_heroes': heroes,
    }

from django.db.models import Sum
from products.models import Product
from orders.models import CustomerOrder
from contact.models import ContactFormSubmission

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
