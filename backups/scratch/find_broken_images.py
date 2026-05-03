import os
import django
from django.conf import settings
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

models_to_check = [
    ('products', 'Product', ['image']),
    ('products', 'Category', ['image']),
    ('products', 'ProductImage', ['image']),
    ('products', 'Collection', ['banner']),
    ('sliders', 'HeroSlider', ['image']),
    ('sliders', 'BannerItem', ['image']),
    ('blog', 'Post', ['image']),
    ('pages', 'GalleryItem', ['image']),
    ('pages', 'Partner', ['logo']),
]

print("--- Checking for images WITHOUT 'media/' prefix ---")

for app_label, model_name, fields in models_to_check:
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        print(f"Skipping {app_label}.{model_name} (not found)")
        continue

    print(f"Checking {model_name}...")
    for obj in model.objects.all():
        for field_name in fields:
            try:
                field_file = getattr(obj, field_name)
                if field_file and field_file.name:
                    if not field_file.name.startswith('media/'):
                        print(f"  Found without prefix: {obj} (ID: {obj.pk}) - {field_name}: {field_file.name}")
                        try:
                            print(f"    URL: {field_file.url}")
                        except Exception as e:
                            print(f"    URL Error: {e}")
            except AttributeError:
                print(f"  Error: {model_name} has no attribute {field_name}")

print("\nDone.")
