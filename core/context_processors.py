from core.models import FrontendDesign, SiteSettings

def theme_context(request):
    theme = FrontendDesign.objects.first()
    return {'theme': theme}

def site_settings(request):
    settings = SiteSettings.objects.first()
    return {'site_settings': settings}
