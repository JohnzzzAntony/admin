from core.models import FrontendDesign

def theme_context(request):
    theme = FrontendDesign.objects.first()
    return {'theme': theme}
