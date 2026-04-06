import os
import django
from django.test import Client
import traceback

try:
    from django.contrib.auth.models import User
    c = Client(HTTP_HOST='localhost')
    u = User.objects.filter(is_superuser=True).first()
    if u:
        c.force_login(u)
    response = c.get('/admin/blog/post/')
    with open('admin_test_out.txt', 'w') as f:
        f.write(f"Status: {response.status_code}\n")
        f.write(response.content.decode('utf-8')[:200])
except Exception as e:
    with open('admin_test_out.txt', 'w') as f:
        f.write(traceback.format_exc())
