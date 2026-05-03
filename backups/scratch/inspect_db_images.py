import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from products.models import Product, Category

print("--- Product Images ---")
for p in Product.objects.all()[:5]:
    print(f"Product: {p.name}")
    print(f"  Image Field: {p.image}")
    try:
        print(f"  Image URL: {p.image.url if p.image else 'N/A'}")
    except Exception as e:
        print(f"  Image URL Error: {e}")
    print(f"  get_image_url: {p.get_image_url}")

print("\n--- Category Images ---")
for c in Category.objects.all()[:5]:
    print(f"Category: {c.name}")
    print(f"  Image Field: {c.image}")
    try:
        print(f"  Image URL: {c.image.url if c.image else 'N/A'}")
    except Exception as e:
        print(f"  Image URL Error: {e}")
    print(f"  get_image_url: {c.get_image_url}")
