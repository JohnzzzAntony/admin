import os
import django
import sys

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jkr.settings")
django.setup()

from django.test import Client, override_settings
from django.urls import reverse
from products.models import Category

@override_settings(ALLOWED_HOSTS=['*'])
def run_tests():
    client = Client()
    
    # Test a few URLs
    urls_to_test = [
        '/',
        reverse('products:product_list'),
    ]

    # Get a category slug if possible
    cat = Category.objects.filter(is_active=True).first()
    if cat:
        urls_to_test.append(cat.get_absolute_url())

    for url in urls_to_test:
        print(f"Testing URL: {url}")
        try:
            response = client.get(url)
            print(f"Status: {response.status_code}")
            if response.status_code == 500:
                print("Server Error detected!")
                # If we get a 500 without an exception, it might be due to templates
                # The test client should raise TemplateSyntaxError etc if DEBUG is True
        except Exception as e:
            import traceback
            print("Caught Exception:")
            traceback.print_exc()
            print("-" * 40)

if __name__ == "__main__":
    run_tests()
