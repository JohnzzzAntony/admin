"""
Django Signals for Email Notifications
Handles: login alerts, order status changes, payment confirmations
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.conf import settings
from django.utils import timezone
import threading
import logging

logger = logging.getLogger(__name__)

def send_async_email(subject, message, to_email):
    """Send email in background thread to avoid blocking"""
    from django.core.mail import send_mail
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        if from_email == 'EMAIL_HOST_USER':
            from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [to_email], fail_silently=True)
        logger.info(f"Email sent to {to_email}: {subject}")
    except Exception as e:
        logger.error(f"Email send failed: {e}")

def get_client_ip(request):
    """Get client IP from request"""
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'Unknown')
    except:
        return 'Unknown'

def send_login_notification(user, request, login_type='email'):
    """Send email notification when user logs in"""
    try:
        site_config = None
        try:
            from core.models import SiteSettings
            site_config = SiteSettings.objects.first()
        except:
            pass

        if site_config and not site_config.enable_email_notifications:
            return

        subject = f"Login Alert - {user.username}"
        message = f\"\"\"
Dear {user.get_full_name() or user.username},

We noticed a new login to your account.

Account Details:
-----------------
Username: {user.username}
Email: {user.email}
Login Type: {login_type.title()}
Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
IP Address: {get_client_ip(request)}

If this was you, no action is required.
If you don't recognize this activity, please secure your account immediately.

Best regards,
Demo International Team
        \"\"\"

        # Send email in background
        if user.email:
            thread = threading.Thread(
                target=send_async_email,
                args=(subject, message.strip(), user.email)
            )
            thread.daemon = True
            thread.start()

    except Exception as e:
        logger.error(f"Login notification error: {e}")

# ── Signal Receivers ──────────────────────────────────────────────────────────

@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    """Triggered when any user logs in"""
    send_login_notification(user, request, login_type='email')
