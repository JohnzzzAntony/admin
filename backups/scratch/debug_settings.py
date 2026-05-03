import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

print(f"IS_PRODUCTION: {getattr(settings, 'IS_PRODUCTION', 'N/A')}")
print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"CLOUDINARY_STORAGE: {settings.CLOUDINARY_STORAGE}")
print(f"STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")

# Check if cloudinary is actually configured
from cloudinary import config as cld_config
c = cld_config()
print(f"Cloudinary Cloud Name: {c.cloud_name}")
print(f"Cloudinary API Key: {c.api_key}")
