import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from products.models import Category

print("Checking Categories and their Image data...")
cats = Category.objects.all()
for cat in cats:
    print(f"[{cat.id}] Name: {cat.name}")
    print(f"  - image_url: '{cat.image_url}'")
    print(f"  - image (file): '{cat.image}'")
    try:
        print(f"  - Final URL from get_image_url: {cat.get_image_url}")
    except Exception as e:
        print(f"  - Error getting URL: {e}")
    print("-" * 20)
