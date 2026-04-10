
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from products.models import Category
print("ID|Name|ParentID|ParentName")
for c in Category.objects.all().order_by('name'):
    p_id = c.parent_id
    p_name = c.parent.name if c.parent else "None"
    print(f"{c.id}|{c.name}|{p_id}|{p_name}")
