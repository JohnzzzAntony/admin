import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from products.models import Category
try:
    cat = Category.objects.create(name="Test Category Bug")
    print(f"Created category: {cat}")
    cat.delete()
    print("Deleted category")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
