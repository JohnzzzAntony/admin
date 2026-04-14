"""
Tabby Payment Integration
Buy Now Pay Later - Pay in 4 installments
https://tabby.ai/
"""
import logging
import hashlib
import hmac
from django.conf import settings
import requests

logger = logging.getLogger(__name__)

TABBY_API_URL = 'https://api.tabby.ai/api/v2'

def get_tabby_config():
    return {
        'api_key': getattr(settings, 'TABBY_API_KEY', ''),
        'secret_key': getattr(settings, 'TABBY_SECRET_KEY', ''),
        'merchant_code': getattr(settings, 'TABBY_MERCHANT_CODE', ''),
    }

class TabbyPayment:
    def __init__(self):
        config = get_tabby_config()
        self.api_key = config['api_key']
        self.secret_key = config['secret_key']
        self.merchant_code = config['merchant_code']
        self.is_test_mode = getattr(settings, 'TABBY_TEST_MODE', True)
        self.api_base = 'https://api.test.tabby.ai' if self.is_test_mode else TABBY_API_URL

    def create_session(self, order, callback_url, cancel_url, success_url):
        """Create a Tabby checkout session"""
        try:
            order_id = f"Demo-{order.pk:05d}"

            # Build line items
            line_items = []
            for item in order.items.all():
                line_items.append({
                    'title': item.product_name,
                    'description': item.product_name,
                    'quantity': item.quantity,
                    'unit_price': str(item.unit_price),
                    'category': 'Other',
                })

            if float(order.shipping_amount) > 0:
                line_items.append({
                    'title': 'Shipping',
                    'description': 'Delivery charges',
                    'quantity': 1,
                    'unit_price': str(order.shipping_amount),
                    'category': 'Other',
                })

            payload = {
                'payment': {
                    'amount': str(order.total_amount),
                    'currency': 'AED',
                    'description': f'Order #{order_id}',
                    'buyer': {
                        'email': order.email,
                        'phone': order.phone,
                        'name': f"{order.first_name} {order.last_name}",
                    },
                    'shipping_address': {
                        'city': order.city,
                        'address': order.street,
                        'zip': '',
                        'country': order.country,
                    },
                    'items': line_items,
                },
                'merchant_code': self.merchant_code,
                'merchant_urls': {
                    'success': success_url,
                    'cancel': cancel_url,
                    'webhook': callback_url,
                },
                'language': 'en',
                'expiry_time': 'PT24H',
            }

            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
            }

            response = requests.post(
                f'{self.api_base}/checkout',
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'checkout_url': data.get('checkout_url', ''),
                    'session_id': data.get('session_id', ''),
                    'payment_id': data.get('payment_id', ''),
                }
            else:
                logger.error(f"Tabby API error: {response.status_code} - {response.text}")
                return {'success': False, 'error': response.text}

        except Exception as e:
            logger.error(f"Tabby session creation error: {e}")
            return {'success': False, 'error': str(e)}

def create_tabby_session(order, request):
    """Convenience function to create Tabby session"""
    tabby = TabbyPayment()

    base_url = settings.SITE_URL
    callback_url = f"{base_url}/orders/tabby/webhook/"
    cancel_url = f"{base_url}/orders/checkout/payment/"
    success_url = f"{base_url}/orders/checkout/success/"

    return tabby.create_session(order, callback_url, cancel_url, success_url)
