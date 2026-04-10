from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
import stripe
from products.models import Product
from .models import QuoteEnquiry, QuoteItem, CustomerOrder, CustomerOrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

def _get_cart_items(request):
    """
    Helper: resolve cart session into list of dicts.
    Cart stores product.id as the unique key.
    """
    cart = request.session.get('enquiry_cart', {})
    items = []
    total_shipping = 0
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            
            qty = int(item_data.get('quantity', 1))
            price_info = product.get_best_price_info()
            
            unit_price = price_info['final_price']
            total_item = round(unit_price * qty, 2)
            
            # Shipping logic
            shipping_per_unit = 0 if product.free_shipping else (product.additional_shipping_charge or 0)
            shipping_item = round(shipping_per_unit * qty, 2)
            total_shipping += shipping_item

            offer_applied = price_info.get('offer')
            bogo_message = None
            if offer_applied and offer_applied.offer_type == 'bogo':
                bogo_message = "BOGO Applied: Buy 1 Get 1 Free"
                payable_qty = (qty // 2) + (qty % 2)
                total_item = round(unit_price * payable_qty, 2)

            items.append({
                'product': product,
                'quantity': qty,
                'unit_price': unit_price,
                'regular_price': price_info['regular_price'],
                'total_item': total_item,
                'shipping_item': shipping_item,
                'is_free_shipping': product.free_shipping,
                'has_offer': price_info['has_offer'],
                'offer_name': offer_applied.name if offer_applied else None,
                'bogo_message': bogo_message,
            })
        except (Product.DoesNotExist, ValueError):
            continue
    return items, round(total_shipping, 2)


# ── Cart ─────────────────────────────────────────────────────────────────────

def enquiry_cart(request):
    cart_items, total_shipping = _get_cart_items(request)
    subtotal = sum(item['total_item'] for item in cart_items)
    grand_total = subtotal + total_shipping
    return render(request, 'orders/enquiry_cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total_shipping': total_shipping,
        'grand_total': grand_total
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    cart = request.session.get('enquiry_cart', {})
    item_key = str(product.id)
    
    if item_key in cart:
        cart[item_key]['quantity'] += 1
    else:
        cart[item_key] = {'quantity': 1}

    request.session['enquiry_cart'] = cart
    messages.success(request, f"✅ {product.name} added to cart.")
    return redirect('orders:enquiry_cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('enquiry_cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
    
    request.session['enquiry_cart'] = cart
    messages.info(request, "Item removed from cart.")
    return redirect('orders:enquiry_cart')


# ── Checkout Step 1 — Billing ─────────────────────────────────────────────────

def checkout_as_guest(request):
    """Sets a session flag to allow checkout without login."""
    request.session['is_guest_checkout'] = True
    return redirect('orders:checkout_billing')

def checkout_billing(request):
    cart_items, total_shipping = _get_cart_items(request)
    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect('orders:enquiry_cart')

    # Auth logic: Must be logged in OR have clicked "Guest Checkout"
    if not request.user.is_authenticated and not request.session.get('is_guest_checkout'):
        from django.urls import reverse
        return redirect(f"{reverse('accounts:login')}?next={request.path}")

    if request.method == 'POST':
        billing = {
            'first_name': request.POST.get('first_name', ''),
            'last_name':  request.POST.get('last_name', ''),
            'email':      request.POST.get('email', ''),
            'phone':      request.POST.get('phone', ''),
            'department': request.POST.get('department', ''),
            'country':    request.POST.get('country', ''),
            'city':       request.POST.get('city', ''),
            'street':     request.POST.get('street', ''),
            'comment':    request.POST.get('comment', ''),
            'trn':        request.POST.get('trn', ''),
            'billing_same': request.POST.get('billing_address_same_as_shipping') == 'on',
            'b_first_name': request.POST.get('billing_first_name', ''),
            'b_last_name':  request.POST.get('billing_last_name', ''),
            'b_email':      request.POST.get('billing_email', ''),
            'b_phone':      request.POST.get('billing_phone', ''),
            'b_country':    request.POST.get('billing_country', ''),
            'b_city':       request.POST.get('billing_city', ''),
            'b_street':     request.POST.get('billing_street', ''),
        }
        request.session['checkout_billing'] = billing
        return redirect('orders:checkout_payment')

    form_data = request.session.get('checkout_billing', {})
    subtotal = sum(item['total_item'] for item in cart_items)
    total_tax = sum((item['total_item'] * item['product'].tax_percentage / 100) for item in cart_items)
    return render(request, 'orders/checkout_billing.html', {
        'cart_items': cart_items,
        'form_data': form_data,
        'subtotal': subtotal,
        'total_tax': total_tax,
        'total_shipping': total_shipping,
        'grand_total': subtotal + total_shipping + total_tax
    })


# ── Checkout Step 2 — Payment ─────────────────────────────────────────────────

def checkout_payment(request):
    cart_items, total_shipping = _get_cart_items(request)
    billing = request.session.get('checkout_billing')

    if not cart_items:
        return redirect('orders:enquiry_cart')
    if not billing:
        return redirect('orders:checkout_billing')

    subtotal = sum(item['total_item'] for item in cart_items)
    total_tax = sum((item['total_item'] * item['product'].tax_percentage / 100) for item in cart_items)
    grand_total = subtotal + total_shipping + total_tax

    if request.method == 'POST':
        import traceback
        from django.utils import timezone
        try:
            payment_method = request.POST.get('payment_method', 'card')

            # Create the CustomerOrder record
            order = CustomerOrder.objects.create(
                user=request.user if request.user.is_authenticated else None,
                is_guest=not request.user.is_authenticated,
                
                # Shipping
                first_name=billing.get('first_name', ''),
                last_name=billing.get('last_name', ''),
                email=billing.get('email', ''),
                phone=billing.get('phone', ''),
                department=billing.get('department', ''),
                country=billing.get('country', ''),
                city=billing.get('city', ''),
                street=billing.get('street', ''),
                comment=billing.get('comment', ''),
                
                # TRN & Billing
                trn=billing.get('trn'),
                billing_address_same_as_shipping=billing.get('billing_same', True),
                billing_first_name=billing.get('b_first_name', ''),
                billing_last_name=billing.get('b_last_name', ''),
                billing_email=billing.get('b_email', ''),
                billing_phone=billing.get('b_phone', ''),
                billing_country=billing.get('b_country', ''),
                billing_city=billing.get('b_city', ''),
                billing_street=billing.get('b_street', ''),

                payment_method=payment_method,
                status='pending',
                payment_status='pending',
                shipping_amount=total_shipping,
                tax_amount=total_tax,
                total_amount=grand_total
            )

            # Save line items
            for item in cart_items:
                product = item['product']
                CustomerOrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    quantity=item['quantity'],
                    regular_price=item.get('regular_price', item['unit_price']),
                    unit_price=item['unit_price'],
                    tax_percentage=product.tax_percentage,
                    shipping_charge=item['shipping_item'],
                    total_price=item['total_item']
                )

            # Clear cart & billing from session
            request.session['enquiry_cart'] = {}
            request.session.pop('checkout_billing', None)

            # Store order id for the success page
            request.session['last_order_id'] = order.id

            if payment_method == 'card':
                # --- STRIPE CHECKOUT INTEGRATION ---
                line_items = []
                for item in cart_items:
                    line_items.append({
                        'price_data': {
                            'currency': 'aed',
                            'product_data': {
                                'name': item['product'].name,
                            },
                            'unit_amount': int(item['unit_price'] * 100), # in fils
                        },
                        'quantity': item['quantity'],
                    })
                
                # Add shipping as a separate line item if > 0
                if total_shipping > 0:
                    line_items.append({
                        'price_data': {
                            'currency': 'aed',
                            'product_data': {
                                'name': 'Shipping Charge',
                            },
                            'unit_amount': int(total_shipping * 100),
                        },
                        'quantity': 1,
                    })

                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('orders:checkout_success')) + "?session_id={CHECKOUT_SESSION_ID}",
                    cancel_url=request.build_absolute_uri(reverse('orders:checkout_payment')),
                    client_reference_id=str(order.id),
                    customer_email=order.email,
                )
                
                # Save session ID to order
                order.stripe_session_id = checkout_session.id
                order.save(update_fields=['stripe_session_id'])
                
                return redirect(checkout_session.url, code=303)
            
            # For COD or other methods, proceed as before
            # Clear cart & billing only for non-stripe here (Stripe will clear on success/webhook)
            request.session['enquiry_cart'] = {}
            request.session.pop('checkout_billing', None)
            return redirect('orders:checkout_success')

        except Exception as e:
            with open('order_error_traceback.log', 'a') as f:
                f.write(f"\n--- ERROR AT {timezone.now()} ---\n")
                f.write(traceback.format_exc())
            messages.error(request, f"❌ Order Processing Failed: {str(e)}")
            return redirect('orders:checkout_payment')

    return render(request, 'orders/checkout_payment.html', {
        'cart_items': cart_items,
        'billing': billing,
        'subtotal': subtotal,
        'total_tax': total_tax,
        'total_shipping': total_shipping,
        'grand_total': grand_total
    })


# ── Checkout Step 3 — Success ─────────────────────────────────────────────────

def checkout_success(request):
    order_id = request.session.pop('last_order_id', None)
    session_id = request.GET.get('session_id')

    if not order_id and not session_id:
        return redirect('orders:enquiry_cart')
        
    if session_id:
        # If we have a session ID, try to find the order by it
        order = get_object_or_404(CustomerOrder, stripe_session_id=session_id)
        # Clear cart for Stripe success (since we didn't clear it in POST)
        request.session['enquiry_cart'] = {}
        request.session.pop('checkout_billing', None)
    else:
        order = get_object_or_404(CustomerOrder, id=order_id)
        
    return render(request, 'orders/checkout_success.html', {
        'order': order,
    })


def download_invoice(request, order_id):
    """
    Public view for customers to download their invoice PDF.
    Basic security: check if order matches user or is the last order in session.
    """
    from .utils import create_invoice_pdf
    
    order = get_object_or_404(CustomerOrder, id=order_id)
    
    # Security check
    is_owner = False
    if request.user.is_authenticated and order.user == request.user:
        is_owner = True
    elif request.session.get('last_order_id') == order.id:
        is_owner = True
    elif request.GET.get('session_id') == order.stripe_session_id:
        is_owner = True
        
    if not is_owner:
        messages.error(request, "You are not authorized to download this invoice.")
        return redirect('core:home')
        
    return create_invoice_pdf(order)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Highly secured webhook listener for Stripe events.
    Verifies the signature to ensure only Stripe can call this.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)
    event = None

    try:
        if endpoint_secret:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        else:
            # Fallback if secret is not set (less secure, only for debugging)
            event = stripe.Event.construct_from(request.json(), stripe.api_key)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Payment is successful. Update the order status.
        order_id = session.get('client_reference_id')
        if order_id:
            try:
                order = CustomerOrder.objects.get(id=order_id)
                order.payment_status = 'paid'
                order.stripe_payment_id = session.get('payment_intent')
                order.save()
                
                # Note: notifications are already triggered on save() if status changes 
                # (handled in CustomerOrder.save)
                
            except CustomerOrder.DoesNotExist:
                pass

    return HttpResponse(status=200)


# ── Legacy enquiry submit (kept for compatibility) ───────────────────────────

def submit_enquiry(request):
    if request.method == 'POST':
        cart = request.session.get('enquiry_cart', {})
        if not cart:
            messages.warning(request, "Your cart is empty.")
            return redirect('orders:enquiry_cart')
        billing = {k: request.POST.get(k, '') for k in
                   ['first_name','last_name','email','department','country','city','street','phone','comment']}
        enquiry = QuoteEnquiry.objects.create(**billing)
        for product_id, item_data in cart.items():
            product = get_object_or_404(Product, id=int(product_id))
            QuoteItem.objects.create(enquiry=enquiry, product=product, quantity=item_data['quantity'])
        request.session['enquiry_cart'] = {}
        # For legacy, we keep using the old success page or redirect to home
        messages.success(request, "Your enquiry has been submitted successfully.")
        return redirect('core:home')
    return redirect('orders:enquiry_cart')
