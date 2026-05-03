import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from products.models import Product, Category, ProductImage, Collection
from sliders.models import HeroSlider, PromoBanner
from pages.models import Page
from blog.models import Post

models_to_check = [
    (Product, ['image']),
    (Category, ['image']),
    (ProductImage, ['image']),
    (Collection, ['banner']),
    (HeroSlider, ['image']),
    (PromoBanner, ['image']),
    (Post, ['image']),
]

print("--- Checking for images WITHOUT 'media/' prefix ---")

for model, fields in models_to_check:
    print(f"Checking {model.__name__}...")
    for obj in model.objects.all():
        for field_name in fields:
            field_file = getattr(obj, field_name)
            if field_file and not field_file.name.startswith('media/'):
                print(f"  Found without prefix: {obj} - {field_name}: {field_file.name}")
                try:
                    print(f"    URL: {field_file.url}")
                except Exception as e:
                    print(f"    URL Error: {e}")

print("\nDone.")
