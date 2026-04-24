import os
import sys
import django
from django.conf import settings

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')

# Override DATABASE_URL to check the SOURCE_DB
SOURCE_DB = "postgresql://neondb_owner:npg_UXBiNGh80Orw@ep-dry-moon-a1owxnuf-pooler.ap-southeast-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require"
os.environ['DATABASE_URL'] = SOURCE_DB

django.setup()

from pages.models import Service

print(f"Checking SOURCE_DB: {SOURCE_DB}")
print(f"Total services: {Service.objects.count()}")
for s in Service.objects.all():
    print(f"ID: {s.id}, Title: {s.title}, Active: {s.is_active}")
