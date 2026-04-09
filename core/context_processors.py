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
