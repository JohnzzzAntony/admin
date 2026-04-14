"""
Tamara Payment Integration
Buy Now Pay Later - Pay in 3 installments
https://tamara.co/
"""
import logging
from django.conf import settings
import requests

logger = logging.getLogger(__name__)

TAMARA_API_URL = 'https://api.tamara.co'

def get_tamara_config():
    return {
        'api_key': getattr(settings, 'TAMARA_API_KEY', ''),
        'api_token': getattr(settings, 'TAMARA_API_TOKEN', ''),
        'merchant_id': getattr(settings, 'TAMARA_MERCHANT_ID', ''),
    }

class TamaraPayment:
    def __init__(self):
        config = get_tamara_config()
        self.api_key = config['api_key']
        self.api_token = config['api_token']
        self.merchant_id = config['merchant_id']
        self.is_test_mode = getattr(settings, 'TAMARA_TEST_MODE', True)
        self.api_base = 'https://api-sandbox.tamara.co' if self.is_test_mode else TAMARA_API_URL

    def create_checkout(self, order, success_url, cancel_url, callback_url):
        """Create a Tamara checkout session"""
        try:
            order_id = f"Demo-{order.pk:05d}"

            line_items = []
            for item in order.items.all():
                line_items.append({
                    'reference_id': str(item.product_id) if item.product else 'unknown',
                    'type': 'physical',
                    'name': item.product_name,
                    'description': item.product_name,
                    'quantity': item.quantity,
                    'unit_price': {
                        'amount': str(item.unit_price),
                        'currency': 'AED',
                    },
                    'tax_amount': {
                        'amount': str(item.tax_amount),
                        'currency': 'AED',
                    },
                })

            if float(order.shipping_amount) > 0:
                line_items.append({
                    'reference_id': 'shipping',
                    'type': 'shipping',
                    'name': 'Shipping & Handling',
                    'description': 'Delivery charges',
                    'quantity': 1,
                    'unit_price': {
                        'amount': str(order.shipping_amount),
                        'currency': 'AED',
                    },
                    'tax_amount': {
                        'amount': '0.00',
                        'currency': 'AED',
                    },
                })

            payload = {
                'country': order.country,
                'order_reference_id': str(order.pk),
                'total_amount': {
                    'amount': str(order.total_amount),
                    'currency': 'AED',
                },
                'description': f'Order #{order_id}',
                'liability': 'tamara',
                'merchant_urls': {
                    'success': success_url,
                    'cancel': cancel_url,
                    'failure': cancel_url,
                    'notification': callback_url,
                },
                'items': line_items,
                'consumer': {
                    'first_name': order.first_name,
                    'last_name': order.last_name,
                    'phone_number': order.phone,
                    'email': order.email,
                },
                'shipping_address': {
                    'first_name': order.first_name,
                    'last_name': order.last_name,
                    'phone_number': order.phone,
                    'address_line1': order.street,
                    'city': order.city,
                    'country_code': 'AE',
                },
            }

            headers = {
                'Authorization': f'Bearer {self.api_token}',
                'Content-Type': 'application/json',
                'Tamara-Api-Key': self.api_key,
                'Merchant-Url': settings.SITE_URL,
            }

            response = requests.post(
                f'{self.api_base}/checkout',
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code in [200, 201]:
                data = response.json()
                checkout_url = data.get('checkout_url', {}).get('url', '') if isinstance(data.get('checkout_url'), dict) else data.get('checkout_url', '')

                return {
                    'success': True,
                    'checkout_url': checkout_url,
                    'tamara_order_id': data.get('order_id', ''),
                    'tamara_reference_id': str(order.pk),
                }
            else:
                logger.error(f"Tamara API error: {response.status_code} - {response.text}")
                return {'success': False, 'error': response.text}

        except Exception as e:
            logger.error(f"Tamara checkout creation error: {e}")
            return {'success': False, 'error': str(e)}

def create_tamara_checkout(order, request):
    """Convenience function to create Tamara checkout"""
    tamara = TamaraPayment()

    base_url = settings.SITE_URL
    callback_url = f"{base_url}/orders/tamara/webhook/"
    cancel_url = f"{base_url}/orders/checkout/payment/"
    success_url = f"{base_url}/orders/checkout/success/?order_id={order.pk}"

    return tamara.create_checkout(order, success_url, cancel_url, callback_url)
