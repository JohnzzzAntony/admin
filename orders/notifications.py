import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from core.models import SiteSettings

logger = logging.getLogger(__name__)

def send_customer_notification(order, is_automated=True):
    """主 logic for multi-channel notifications."""
    try:
        site_config = SiteSettings.objects.first()
        if not site_config:
            return

        order_id = f"Demo-{order.pk:05d}"
        customer_name = f"{order.first_name} {order.last_name}"
        status_label = order.get_status_display()
        tracking_link = f"{settings.SITE_URL}/orders/track/{order.pk}/" # Placeholder
        
        message_body = (
            f"Dear {customer_name},\n\n"
            f"Update for your Order #{order_id}: Your order status is now '{status_label}'.\n\n"
            f"Track your order here: {tracking_link}\n\n"
            f"Thank you for choosing Demo International."
        )

        # 1. Email Channel
        if site_config.enable_email_notifications:
            import threading
            
            def send_async_email(subject, message, to_email):
                try:
                    # Resolve from_email - ensure it's a real email, not a config key string
                    from_email = settings.DEFAULT_FROM_EMAIL
                    if from_email == 'EMAIL_HOST_USER':
                        from_email = settings.EMAIL_HOST_USER

                    send_mail(
                        subject,
                        message,
                        from_email,
                        [to_email],
                        fail_silently=True, # Critical: never block main thread
                    )
                    logger.info(f"Email sent for order {order_id}")
                except Exception as e:
                    logger.error(f"Email failure: {e}")

            # Start notification in background
            email_thread = threading.Thread(
                target=send_async_email,
                args=(f"Order #{order_id} Update — {status_label}", message_body, order.email)
            )
            email_thread.daemon = True
            email_thread.start()

        # 2. SMS Channel (Stub)
        if site_config.enable_sms_notifications:
            # Integration logic for SMS provider (e.g. Twilio)
            # send_sms(order.phone, message_body)
            logger.info(f"SMS notification triggered for {order_id} (Providers to be integrated)")

        # 3. WhatsApp Channel (Stub)
        if site_config.enable_whatsapp_notifications:
            # Integration logic for WhatsApp (e.g. Twilio WhatsApp API)
            # send_whatsapp(order.phone, message_body)
            logger.info(f"WhatsApp notification triggered for {order_id} (Providers to be integrated)")

    except Exception as e:
        logger.error(f"Notification error: {e}")
