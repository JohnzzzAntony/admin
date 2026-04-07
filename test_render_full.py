import os
import django
from django.template import loader
from django.test import RequestFactory

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from products.models import Category, Product
from products.views import category_detail

def test_rendering():
    rf = RequestFactory()
    cat = Category.objects.filter(is_active=True).first()
    if not cat:
        print("No active categories found.")
        return
    
    print(f"DEBUG: Category Found: {cat.name} (Slug: {cat.slug})")
    request = rf.get(f'/category/{cat.slug}/')
    # Add necessary context processors manually if needed, or use the real view
    try:
        from django.contrib.sessions.middleware import SessionMiddleware
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()
        
        # We need site_settings and other context processors
        response = category_detail(request, slug=cat.slug)
        print(f"DEBUG: Status Code: {response.status_code}")
        # print(response.content.decode('utf-8')[:500]) # Preview
    except Exception as e:
        import traceback
        print("RENDER FAIL:")
        traceback.print_exc()

if __name__ == "__main__":
    test_rendering()
