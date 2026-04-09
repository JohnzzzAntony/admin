import os
import django
import random
import string
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from products.models import Product

products = Product.objects.filter(sku_id='')
print(f'Found {products.count()} products with empty SKU.')

for p in products:
    prefix = slugify(p.name)[:10].upper()
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    p.sku_id = f"FIX-{prefix}-{suffix}"
    try:
        p.save()
        print(f"Updated: {p.name} -> {p.sku_id}")
    except Exception as e:
        print(f"Failed to update {p.name}: {e}")

print('Finished fixing SKUs.')
