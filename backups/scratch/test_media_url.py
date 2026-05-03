import os
import django
from django.conf import settings

# Mock settings for testing
os.environ['CLOUDINARY_CLOUD_NAME'] = 'test_cloud'
os.environ['CLOUDINARY_API_KEY'] = 'test_key'
os.environ['CLOUDINARY_API_SECRET'] = 'test_secret'

# We need to configure settings before django.setup()
from django.conf import settings

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=['cloudinary', 'cloudinary_storage'],
        CLOUDINARY_STORAGE={
            'CLOUD_NAME': 'test_cloud',
            'API_KEY': 'test_key',
            'API_SECRET': 'test_secret',
        },
        MEDIA_URL='/', # Testing this
        DEFAULT_FILE_STORAGE='cloudinary_storage.storage.MediaCloudinaryStorage'
    )

import django
django.setup()

from django.core.files.storage import get_storage_class
media_storage = get_storage_class()()

print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"URL for 'media/products/test.jpg': {media_storage.url('media/products/test.jpg')}")
