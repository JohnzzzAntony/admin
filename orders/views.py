from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import QuoteEnquiry, QuoteItem, CustomerOrder, CustomerOrderItem


def _get_cart_items(request):
    """Helper: resolve cart session into list of dicts."""
    cart = request.session.get('enquiry_cart', {})
    items = []
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            price = float(item_data.get('price', 0))
            qty = int(item_data.get('quantity', 1))
            items.append({
                'product': product,
                'quantity': qty,
                'price': price,
                'total_item': round(price * qty, 2),
            })
        except Product.DoesNotExist:
            continue
    return items


# ── Cart ─────────────────────────────────────────────────────────────────────

def enquiry_cart(request):
    cart_items = _get_cart_items(request)
    return render(request, 'orders/enquiry_cart.html', {'cart_items': cart_items})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('enquiry_cart', {})

    # Use sale_price if set and > 0, else regular_price
    rp = product.regular_price or 0
    sp = product.sale_price or 0
    price = float(sp if sp and sp > 0 else rp)

    str_id = str(product_id)
    if str_id in cart:
        cart[str_id]['quantity'] += 1
    else:
        cart[str_id] = {'quantity': 1, 'price': str(price)}

    request.session['enquiry_cart'] = cart
    messages.success(request, f"✅ {product.name} added to cart.")
    return redirect('enquiry_cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('enquiry_cart', {})
    str_id = str(product_id)
    if str_id in cart:
        del cart[str_id]
        request.session['enquiry_cart'] = cart
        messages.info(request, "Item removed from cart.")
    return redirect('enquiry_cart')


# ── Checkout Step 1 — Billing ─────────────────────────────────────────────────

def checkout_billing(request):
    cart_items = _get_cart_items(request)
    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect('enquiry_cart')

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
        }
        request.session['checkout_billing'] = billing
        return redirect('checkout_payment')

    form_data = request.session.get('checkout_billing', {})
    return render(request, 'orders/checkout_billing.html', {
        'cart_items': cart_items,
        'form_data': form_data,
    })


# ── Checkout Step 2 — Payment ─────────────────────────────────────────────────

def checkout_payment(request):
    cart_items = _get_cart_items(request)
    billing = request.session.get('checkout_billing')

    if not cart_items:
        return redirect('enquiry_cart')
    if not billing:
        return redirect('checkout_billing')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'card')

        # Create the CustomerOrder record
        order = CustomerOrder.objects.create(
            first_name=billing.get('first_name', ''),
            last_name=billing.get('last_name', ''),
            email=billing.get('email', ''),
            phone=billing.get('phone', ''),
            department=billing.get('department', ''),
            country=billing.get('country', ''),
            city=billing.get('city', ''),
            street=billing.get('street', ''),
            comment=billing.get('comment', ''),
            payment_method=payment_method,
            status='pending',
            payment_status='pending'
        )

        # Save line items
        total_amount = 0
        for item in cart_items:
            product = item['product']
            CustomerOrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=item['quantity'],
                unit_price=item['price'],
                total_price=item['total_item']
            )
            total_amount += item['total_item']
        
        # Update total amount
        order.total_amount = total_amount
        order.save()

        # Clear cart & billing from session
        request.session['enquiry_cart'] = {}
        request.session.pop('checkout_billing', None)

        # Store order id for the success page
        request.session['last_order_id'] = order.id

        return redirect('checkout_success')

    return render(request, 'orders/checkout_payment.html', {
        'cart_items': cart_items,
        'billing': billing,
    })


# ── Checkout Step 3 — Success ─────────────────────────────────────────────────

def checkout_success(request):
    order_id = request.session.pop('last_order_id', None)
    if not order_id:
        return redirect('enquiry_cart')
        
    order = get_object_or_404(CustomerOrder, id=order_id)
    return render(request, 'orders/checkout_success.html', {
        'order': order,
    })


# ── Legacy enquiry submit (kept for compatibility) ───────────────────────────

def submit_enquiry(request):
    if request.method == 'POST':
        cart = request.session.get('enquiry_cart', {})
        if not cart:
            messages.warning(request, "Your cart is empty.")
            return redirect('enquiry_cart')
        billing = {k: request.POST.get(k, '') for k in
                   ['first_name','last_name','email','department','country','city','street','phone','comment']}
        enquiry = QuoteEnquiry.objects.create(**billing)
        for product_id, item_data in cart.items():
            product = get_object_or_404(Product, id=int(product_id))
            QuoteItem.objects.create(enquiry=enquiry, product=product, quantity=item_data['quantity'])
        request.session['enquiry_cart'] = {}
        # For legacy, we keep using the old success page or redirect to home
        messages.success(request, "Your enquiry has been submitted successfully.")
        return redirect('home')
    return redirect('enquiry_cart')
