
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from products.models import Product, Category
print("Product Name | Cat ID | Cat Name | Cat Parent")
for p in Product.objects.all().order_by('-id')[:50]:
    c = p.category
    if c:
        p_name = c.parent.name if c.parent else "None"
        print(f"{p.name[:40]} | {c.id} | {c.name} | {p_name}")
    else:
        print(f"{p.name[:40]} | None | None | None")
