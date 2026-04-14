import logging
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from core.models import SiteSettings

logger = logging.getLogger(__name__)

def send_customer_notification(order, is_automated=True, notification_type='status_change'):
    """Main logic for multi-channel notifications.

    Args:
        order: CustomerOrder instance
        is_automated: Whether this is an automated notification
        notification_type: 'status_change', 'payment_confirmation', 'order_placed'
    """
    try:
        site_config = SiteSettings.objects.first()
        if not site_config:
            logger.warning("No SiteSettings found for notifications")
            return

        order_id = f"Demo-{order.pk:05d}"
        customer_name = f"{order.first_name} {order.last_name}"
        status_label = order.get_status_display()
        tracking_link = f"{settings.SITE_URL}/orders/track/{order.pk}/"

        # Customize message based on notification type
        if notification_type == 'payment_confirmation':
            subject_prefix = "Payment Confirmed"
            message_body = f"""
Dear {customer_name},

Great news! Your payment has been successfully processed.

Order Details:
---------------
Order Number: #{order_id}
Total Amount: {order.total_amount} {settings.CURRENCY}
Payment Method: {order.get_payment_method_display()}
Payment Status: Paid

Shipping Address:
{order.street}, {order.city}, {order.country}
Phone: {order.phone}

Track your order: {tracking_link}

Thank you for choosing {site_config.site_name}!
            """.strip()

        elif notification_type == 'order_placed':
            subject_prefix = "Order Received"
            message_body = f"""
Dear {customer_name},

Thank you for your order! We have received your order and it is being processed.

Order Details:
---------------
Order Number: #{order_id}
Total Amount: {order.total_amount} {settings.CURRENCY}
Payment Method: {order.get_payment_method_display()}
Status: {status_label}

Shipping Address:
{order.street}, {order.city}, {order.country}
Phone: {order.phone}

Track your order: {tracking_link}

We will send you updates as your order progresses.

Thank you for choosing {site_config.site_name}!
            """.strip()

        else:  # status_change
            status_messages = {
                'pending': 'Your order has been received and is being processed.',
                'packaging': 'Your order is being carefully packaged.',
                'ready_for_shipment': 'Your order is ready and awaiting shipment.',
                'shipped': 'Your order has been shipped! It is on its way to you.',
                'delivered': 'Your order has been delivered. We hope you enjoy your purchase!',
                'return_to_origin': 'Your order is being returned to sender.',
                'refund': 'Your refund is being processed.',
            }
            status_message = status_messages.get(order.status, f'Your order status is now: {status_label}')

            subject_prefix = f"Order Update - {status_label}"
            message_body = f"""
Dear {customer_name},

{status_message}

Order Details:
---------------
Order Number: #{order_id}
Current Status: {status_label}
Total Amount: {order.total_amount} {settings.CURRENCY}

Shipping To:
{order.street}, {order.city}, {order.country}
Phone: {order.phone}

Track your order: {tracking_link}

Thank you for choosing {site_config.site_name}!
            """.strip()

        full_subject = f"{subject_prefix} - Order #{order_id}"

        # Email Channel
        if site_config.enable_email_notifications:
            def send_async_email(subject, message, to_email):
                try:
                    from_email = settings.DEFAULT_FROM_EMAIL
                    if from_email == 'EMAIL_HOST_USER':
                        from_email = settings.EMAIL_HOST_USER

                    send_mail(
                        subject,
                        message,
                        from_email,
                        [to_email],
                        fail_silently=True,
                    )
                    logger.info(f"Email sent for order {order_id}: {subject}")
                except Exception as e:
                    logger.error(f"Email failure: {e}")

            # Start notification in background thread
            import threading
            email_thread = threading.Thread(
                target=send_async_email,
                args=(full_subject, message_body, order.email)
            )
            email_thread.daemon = True
            email_thread.start()

        # SMS Channel (Placeholder - requires Twilio/nexmo integration)
        if site_config.enable_sms_notifications and order.phone:
            logger.info(f"SMS notification triggered for {order_id}")

        # WhatsApp Channel (Placeholder)
        if site_config.enable_whatsapp_notifications and order.phone:
            logger.info(f"WhatsApp notification triggered for {order_id}")

    except Exception as e:
        logger.error(f"Notification error: {e}")
