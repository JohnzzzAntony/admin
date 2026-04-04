def site_settings(request):
    from .models import SiteSettings
    from pages.models import PageHero
    
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
    
    # Hero settings for all pages
    try:
        heroes = {hero.page: hero for hero in PageHero.objects.all()}
    except:
        heroes = {}
        
    return {
        'site_settings': settings,
        'page_heroes': heroes,
    }
