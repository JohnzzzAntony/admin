from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Cart (both paths for compatibility)
    path('cart/', views.enquiry_cart, name='enquiry_cart'),
    path('enquiry-cart/', views.enquiry_cart),          # legacy redirect

    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/guest/', views.checkout_as_guest, name='checkout_as_guest'),

    # Checkout flow
    path('checkout/billing/', views.checkout_billing, name='checkout_billing'),
    path('checkout/payment/', views.checkout_payment, name='checkout_payment'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('order/<int:order_id>/invoice/download/', views.download_invoice, name='download_invoice'),

    # Payment Webhooks
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('tabby/webhook/', views.tabby_webhook, name='tabby_webhook'),
    path('tamara/webhook/', views.tamara_webhook, name='tamara_webhook'),

    # Legacy
    path('submit-enquiry/', views.submit_enquiry, name='submit_enquiry'),
]
