import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from django.test import RequestFactory
from products.views import category_detail
from products.models import Category
import traceback

def test_view():
    rf = RequestFactory()
    cat = Category.objects.filter(is_active=True).first()
    if not cat:
        print("No active categories found.")
        return
    
    print(f"Testing category: {cat.name} (slug: {cat.slug})")
    request = rf.get(f'/category/{cat.slug}/')
    
    try:
        response = category_detail(request, slug=cat.slug)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 500:
            print("Received 500 Error!")
    except Exception:
        print("Exception caught:")
        traceback.print_exc()

if __name__ == "__main__":
    test_view()
