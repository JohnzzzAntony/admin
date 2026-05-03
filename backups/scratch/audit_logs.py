import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

logs = LogEntry.objects.all().order_by('-action_time')[:50]
for l in logs:
    print(f"{l.action_time} | {l.content_type.model} | {l.object_repr} | {l.get_action_flag_display()}")
