from core.models import FrontendDesign, SiteSettings
from pages.models import PageHero

def theme_context(request):
    theme = FrontendDesign.objects.first()
    return {'theme': theme}

def site_settings(request):
    settings = SiteSettings.objects.first()
    return {'site_settings': settings}

def page_heroes(request):
    """Provides a dictionary of all PageHero settings indexed by 'page' slug."""
    heroes = {hero.page: hero for hero in PageHero.objects.all()}
    return {'page_heroes': heroes}
