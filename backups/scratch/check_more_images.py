import os
import django
from django.conf import settings
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

def check_model(app, model_name, field):
    try:
        model = apps.get_model(app, model_name)
        print(f"\n--- {model_name} ---")
        for obj in model.objects.all():
            val = getattr(obj, field)
            if val:
                print(f"ID {obj.pk}: {val.name}")
                try:
                    print(f"  URL: {val.url}")
                except Exception as e:
                    print(f"  URL Error: {e}")
            else:
                print(f"ID {obj.pk}: Empty")
    except Exception as e:
        print(f"Error checking {model_name}: {e}")

check_model('sliders', 'HeroSlider', 'image')
check_model('sliders', 'BannerItem', 'image')
check_model('pages', 'PageHero', 'hero_image')
check_model('blog', 'Post', 'featured_image')
