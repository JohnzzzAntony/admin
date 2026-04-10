
import os
import sys
import django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from products.models import Product, Category
from products.forms import ProductAdminForm
from django.contrib.admin.sites import AdminSite

# Mocking the admin save
def test_admin_save():
    print("Testing Product Admin Form Save...")
    cat = Category.objects.filter(parent__isnull=False).first()
    if not cat:
        print("No subcategories found, skipping specific test.")
        cat = Category.objects.first()
        
    data = {
        'name': 'Crash Test Product',
        'parent_category': cat.parent.id if cat and cat.parent else None,
        'category': cat.id if cat else None,
        'quantity': 10,
        'shipping_status': 'available',
        # Add minimal required fields
    }
    
    form = ProductAdminForm(data=data)
    if form.is_valid():
        print("Form is valid. Attempting save...")
        product = form.save(commit=False)
        product.save()
        print(f"Product saved! ID: {product.id}, SKU: {product.sku_id}")
    else:
        print("Form validation failed:")
        print(form.errors)

if __name__ == '__main__':
    try:
        test_admin_save()
    except Exception as e:
        print("!!! CRASH DETECTED !!!")
        import traceback
        traceback.print_exc()
