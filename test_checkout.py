import os
import django
from django.test import Client
import traceback

try:
    c = Client(HTTP_HOST='localhost')
    
    # Let's add something to cart
    from products.models import Product
    p = Product.objects.first()
    if not p:
        print("No product found")
    else:
        # 1. Add to cart
        c.get(f'/enquiry-cart/add/{p.id}/')
        
        # 2. Checkout
        c.get('/enquiry-cart/checkout/guest/')
        
        # 3. Post billing
        billing_resp = c.post('/enquiry-cart/checkout/billing/', {
            'first_name': 'Test',
            'last_name': 'Test',
            'email': 'test@test.com',
            'phone': '123',
            'country': 'US',
            'city': 'NY'
        })
        
        # 4. Post payment
        payment_resp = c.post('/enquiry-cart/checkout/payment/', {
            'payment_method': 'cod'
        })
        
        # Follow the redirect to checkout success
        if payment_resp.status_code == 302:
            success_resp = c.get(payment_resp.url)
            with open('checkout_test_out.txt', 'w') as f:
                f.write(f"Success GET Status: {success_resp.status_code}\n")
                if success_resp.status_code == 500:
                    # Let's just catch the traceback if it fails in python instead of Client
                    pass
        else:
            with open('checkout_test_out.txt', 'w') as f:
                f.write(f"Payment POST Status: {payment_resp.status_code}\n")
                f.write(payment_resp.content.decode('utf-8')[:500])

except Exception as e:
    with open('checkout_test_out.txt', 'w') as f:
        f.write(traceback.format_exc())
