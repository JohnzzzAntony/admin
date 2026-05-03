import os
import django
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

project_root = r'c:\Users\johns\Videos\Projects\Pro'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM pages_service")
    count = cursor.fetchone()[0]
    print(f"Total services in DB table: {count}")
    
    cursor.execute("SELECT id, title FROM pages_service")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]} | Title: {row[1]}")
