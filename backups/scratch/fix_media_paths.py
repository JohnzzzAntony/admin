import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from products.models import Product, Category, ProductImage, Collection
from sliders.models import HeroSlider, PromoBanner
from pages.models import Page
from accounts.models import User # If any profile pics
from blog.models import Post

models_to_fix = [
    (Product, ['image']),
    (Category, ['image']),
    (ProductImage, ['image']),
    (Collection, ['banner']),
    (HeroSlider, ['image']),
    (PromoBanner, ['image']),
    (Post, ['image']),
]

print("--- Fixing Media Paths ---")

for model, fields in models_to_fix:
    print(f"Checking {model.__name__}...")
    count = 0
    for obj in model.objects.all():
        updated = False
        for field_name in fields:
            field_file = getattr(obj, field_name)
            if field_file and field_file.name.startswith('media/'):
                print(f"  Fixing {obj}: {field_name} ({field_file.name} -> {field_file.name[6:]})")
                field_file.name = field_file.name[6:]
                updated = True
        if updated:
            obj.save()
            count += 1
    print(f"  Updated {count} records.")

print("\nDone.")
