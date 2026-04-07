import os
import django
import sys

# Setup Django atmosphere
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from core.models import SiteSettings, StoreLocation
from pages.models import AboutUs
from core.design_models import DesignSettings

def init_demo_site():
    print("Initializing your Demo Site...")
    
    # 1. Site Settings
    site, created = SiteSettings.objects.get_or_create(id=1, defaults={
        'site_name': 'Demo site',
        'email': 'demo@example.com',
        'phone': '+971 00 000 0000',
        'dubai_address': 'Demo Store Address, Dubai, UAE',
    })
    if not created:
        site.site_name = 'Demo site'
        site.save()
    print(f"Site Settings: {site.site_name} (Ready)")

    # 2. Design Settings
    design, created = DesignSettings.objects.get_or_create(id=1, defaults={
        'primary_color': '#2c3e50',
        'secondary_color': '#e74c3c',
        'font_body': "'Outfit', sans-serif",
        'font_heading': "'Outfit', sans-serif",
    })
    print(f"Design Settings: ID 1 (Ready)")

    # 3. About Us (Required for some template parts)
    about, created = AboutUs.objects.get_or_create(id=1, defaults={
        'title': 'Welcome to Demo Site',
        'content': '<p>This is a fresh installation developed for professional store management.</p>',
    })
    print(f"About Us Section: (Ready)")

    print("\nSUCCESS: Your fresh Demo Site is initialized.")
    print("Frontend should now open correctly!")

if __name__ == "__main__":
    init_demo_site()
