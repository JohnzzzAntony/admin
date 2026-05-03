import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from django.core.files.storage import get_storage_class
media_storage = get_storage_class()()

print(f"Storage class: {media_storage.__class__}")
print(f"URL for 'test.jpg': {media_storage.url('test.jpg')}")
print(f"URL for 'products/test.jpg': {media_storage.url('products/test.jpg')}")
