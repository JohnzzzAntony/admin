def site_settings(request):
    from .models import SiteSettings
    from .design_models import DesignSettings
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
        
    try:
        design = DesignSettings.objects.first()
    except:
        design = None
        
    return {
        'site_settings': settings,
        'design_settings': design,
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
