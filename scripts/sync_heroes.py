import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from pages.models import PageHero

def sync_heroes():
    pages = [
        ('about', 'About Us', 'We craft solutions that enhance and simplify lives.'),
        ('products', 'Our Products', 'Explore our wide range of premium products.'),
        ('services', 'Our Services', 'Professional services tailored to your needs.'),
        ('gallery', 'Gallery', 'A glimpse into our work and achievements.'),
        ('stores', 'Our Stores', 'Find a JKR store near you.'),
        ('blog', 'Latest News', 'Stay updated with our latest stories and articles.'),
        ('contact', 'Contact Us', 'Have questions? We would love to hear from you.'),
    ]
    
    for page_code, title, subtitle in pages:
        hero, created = PageHero.objects.get_or_create(
            page=page_code,
            defaults={
                'title': title,
                'subtitle': subtitle,
            }
        )
        if created:
            print(f"Created hero for {page_code}")
        else:
            # Update subtitle if it's empty
            if not hero.subtitle:
                hero.subtitle = subtitle
                hero.save()
                print(f"Updated hero for {page_code}")
            else:
                print(f"Hero for {page_code} already exists")

if __name__ == "__main__":
    sync_heroes()
