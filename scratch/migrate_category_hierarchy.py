
import os
import sys
import django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from products.models import Category, Product
from django.db import transaction

# Map of child keywords to parent category names
AUTO_LINK_MAP = {
    'Wheelchair': 'Wheelchairs',
    'Compression': 'Compression Stockings',
    'Surgical': 'Surgical Supplies',
    'Medical': 'Medical Equipment',
    'Furniture': 'Hospital Furniture',
    'Diagnostic': 'Diagnostic Tools',
    'Laboratory': 'Laboratory',
    'Consumable': 'Consumables',
}

def log(msg):
    print(msg)
    sys.stdout.flush()

def migrate_data():
    log("Starting Database Hierarchy Update...")
    
    with transaction.atomic():
        # 1. Explicit ID Merges for duplicates
        # Homecare (24) -> Home Care (66)
        c24 = Category.objects.filter(id=24).first()
        c66 = Category.objects.filter(id=66).first()
        if c24 and c66:
            log("Merging Homecare into Home Care...")
            Product.objects.filter(category=c24).update(category=c66)
            Category.objects.filter(parent=c24).update(parent=c66)
            c24.delete()

        # Hospital Equipment & Furniture (25) -> Hospital Furniture (65)
        c25 = Category.objects.filter(id=25).first()
        c65 = Category.objects.filter(id=65).first()
        if c25 and c65:
            log("Merging Hospital Equipment into Hospital Furniture...")
            Product.objects.filter(category=c25).update(category=c65)
            Category.objects.filter(parent=c25).update(parent=c65)
            c25.delete()

        # 2. Duplicate Wheelchairs Merge
        # We saw two 'Wheelchairs' root categories.
        wheelchairs = list(Category.objects.filter(name__iexact='Wheelchairs', parent__isnull=True))
        if len(wheelchairs) > 1:
            log(f"Found {len(wheelchairs)} duplicate Wheelchair categories. Merging...")
            target = wheelchairs[0]
            others = wheelchairs[1:]
            for other in others:
                Product.objects.filter(category=other).update(category=target)
                Category.objects.filter(parent=other).update(parent=target)
                other.delete()

        # 3. Auto-Keyword Linking for orphans
        log("Starting Auto-Keyword Linking...")
        all_cats = list(Category.objects.all())
        for cat in all_cats:
            if cat.parent_id is not None:
                continue # Already has a parent
                
            # Skip if it's one of the master parents
            is_master = any(cat.name.strip().lower() == v.lower() for v in AUTO_LINK_MAP.values())
            if is_master:
                continue
                
            for keyword, parent_name in AUTO_LINK_MAP.items():
                if keyword.lower() in cat.name.lower():
                    parent = next((p for p in all_cats if p.name.strip().lower() == parent_name.lower()), None)
                    if parent and cat.id != parent.id:
                        log(f"Linking '{cat.name}' to parent '{parent.name}'")
                        cat.parent = parent
                        cat.save()
                        break

    log("Database Synchronization Complete!")

if __name__ == '__main__':
    migrate_data()
