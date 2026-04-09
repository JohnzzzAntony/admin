def cart_count(request):
    cart = request.session.get('enquiry_cart', {})
    try:
        count = sum(int(item.get('quantity', 0)) for item in cart.values() if isinstance(item, dict))
    except (TypeError, ValueError):
        count = 0
    return {
        'cart_count': count or None  # None is falsy → badge is hidden when cart is empty
    }
