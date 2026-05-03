import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from products.models import Category, Product

def update_all_counts():
    print("Starting product count initialization...")
    # Update leaf categories first, then propagate up
    # Actually, a simple way is to loop through all categories and call the sync logic
    # But since my logic in signals is recursive, I just need to call it for all leaves
    
    categories = Category.objects.all()
    for cat in categories:
        child_ids = [c.id for c in cat.get_all_children(include_self=True)]
        count = Product.objects.filter(category_id__in=child_ids, is_active=True).count()
        cat.product_count = count
        cat.save(update_fields=['product_count'])
        print(f"Updated {cat.name}: {count} products")

if __name__ == "__main__":
    update_all_counts()
