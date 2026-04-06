import os
import django

# We are already in manage.py shell, so django is set up.
from django.test import Client
import traceback

try:
    c = Client(HTTP_HOST='localhost')
    response = c.get('/')
    with open('test_render_out.txt', 'w') as f:
        f.write(f"Status: {response.status_code}\n")
        f.write(response.content.decode('utf-8')[:200])
except Exception as e:
    with open('test_render_out.txt', 'w') as f:
        f.write(traceback.format_exc())
