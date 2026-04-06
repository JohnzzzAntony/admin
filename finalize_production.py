import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from core.models import SiteSettings
from core.design_models import DesignSettings
from pages.models import PageHero

def finalize():
    print("🚀 Finalizing production setup...")
    
    # 1. Initialize DesignSettings if empty
    design, created = DesignSettings.objects.get_or_create(id=1)
    if created:
        print("Created default DesignSettings.")
        design.site_name = "Demo International"
        design.header_title = "Demo International"
        design.header_subtitle = "Elevating Standards in Quality & Global Trade"
        # Set defaults for home sections
        design.hp_collections_title = "Our Collections"
        design.hp_categories_title = "Shop by Categories"
        design.save()
    else:
        print("DesignSettings already exists.")

    # 2. Sync Page Heroes (from sync_heroes.py logic)
    print("Syncing page heroes...")
    pages = [
        ('about', 'About Us', 'We craft solutions that enhance and simplify lives.'),
        ('products', 'Our Products', 'Explore our wide range of premium products.'),
        ('services', 'Our Services', 'Professional services tailored to your needs.'),
        ('gallery', 'Gallery', 'A glimpse into our work and achievements.'),
        ('stores', 'Our Stores', 'Find a store near you.'),
        ('blog', 'Latest News', 'Stay updated with our latest stories.'),
        ('contact', 'Contact Us', 'We would love to hear from you.'),
    ]
    for page_code, title, subtitle in pages:
        HeroType = PageHero
        hero, created = HeroType.objects.get_or_create(page=page_code, defaults={'title': title, 'subtitle': subtitle})
        if created:
             print(f"Created hero for {page_code}")

    # 3. Create initial SiteSettings if missing
    site, created = SiteSettings.objects.get_or_create(id=1, defaults={'site_name': 'Demo International'})
    if created:
        print("Created initial SiteSettings.")

    print("\n✅ Production database finalized.")

if __name__ == "__main__":
    finalize()
