import os
import django
from django.test import Client
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS.append('testserver')

client = Client()

urls_to_test = [
    '/',
    '/products/',
    '/products/category/Active-Wheelchair/',
    '/products/Chair/',
]

for url in urls_to_test:
    print(f"Testing URL: {url}")
    try:
        response = client.get(url)
        print(f"Status: {response.status_code}")
        if response.status_code == 500:
            print("Error detected! Content snippet:")
            print(response.content[:1000].decode('utf-8'))
    except Exception as e:
        print(f"Exception during GET: {e}")
        import traceback
        traceback.print_exc()
