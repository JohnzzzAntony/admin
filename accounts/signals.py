"""
accounts/signals.py  ← REPLACE your existing file
===================================================
Login alert now delegates to email_notifications.send_login_alert()
so all e-mail templates live in one place.
"""

import logging

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    """Send a login-alert e-mail every time any user signs in."""
    try:
        from .email_notifications import send_login_alert
        send_login_alert(user, request)
    except Exception as exc:
        logger.error("on_user_login signal error: %s", exc)
