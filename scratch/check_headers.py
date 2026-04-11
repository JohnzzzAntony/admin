import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.admin import ProductResource

resource = ProductResource()
print("Headers:", resource.get_export_headers())
