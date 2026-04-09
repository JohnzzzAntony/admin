from django.contrib import admin, messages
from django.utils.html import mark_safe, format_html
from django.conf import settings
from django.db.models import Q
from django.conf import settings
from .models import CustomerOrder, CustomerOrderItem, OrderStatusHistory


# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_order_rank(order):
    """
    Returns the 1-based order count for a customer identified by email OR phone.
    """
    ids = list(
        CustomerOrder.objects.filter(
            Q(email__iexact=order.email) | Q(phone=order.phone)
        ).order_by('created_at').values_list('id', flat=True)
    )
    try:
        return ids.index(order.id) + 1
    except ValueError:
        return 1


def _badge(label, color):
    return mark_safe(
        f'<span style="background:{color};color:#fff;padding:3px 10px;'
        f'border-radius:12px;font-size:11px;font-weight:700;white-space:nowrap;">{label}</span>'
    )


# ─── Status colour maps ───────────────────────────────────────────────────────

ORDER_STATUS_COLORS = {
    'pending':            '#ffc107',
    'packaging':          '#fd7e14',
    'ready_for_shipment': '#007bff',
    'shipped':            '#6f42c1',
    'delivered':          '#28a745',
    'return_to_origin':    '#e83e8c',
    'refund':             '#dc3545',
}

PAYMENT_STATUS_COLORS = {
    'pending':  '#ffc107',
    'paid':     '#28a745',
    'failed':   '#dc3545',
    'refunded': '#6c757d',
}

PAYMENT_METHOD_ICONS = {
    'card':   '💳',
    'tabby':  '🟢',
    'tamara': '🟠',
    'cod':    '💵',
}


# ─── Customer Order Items Inline ───────────────────────────────────────────────

class CustomerOrderItemInline(admin.TabularInline):
    model = CustomerOrderItem
    extra = 0
    fields = ('product', 'product_name', 'quantity', 'regular_price', 'unit_price', 'shipping_charge', 'total_price')
    readonly_fields = ('total_price',)

    def has_add_permission(self, request, obj=None):
        return True


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('status_badge', 'changed_at')
    can_delete = False
    
    def status_badge(self, obj):
        color = ORDER_STATUS_COLORS.get(obj.status, '#888')
        # We need a proper way to get the display name.
        # Since 'status' is a field in OrderStatusHistory, we can use the main model's choices.
        # But here 'status' is just a CharField.
        # Let's map it back or just use the badge helper.
        label = dict(CustomerOrder.ORDER_STATUS_CHOICES).get(obj.status, obj.status)
        return _badge(label, color)
    status_badge.short_description = "Status"

    def has_add_permission(self, request, obj=None):
        return False




# ─── Custom Filters ───────────────────────────────────────────────────────────

from django.utils import timezone
from datetime import timedelta

class CreatedAtRangeFilter(admin.SimpleListFilter):
    title = 'date ordered'
    parameter_name = 'created_at_custom'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('yesterday', 'Yesterday'),
            ('7_days', 'Past 7 days'),
            ('30_days', 'Past 30 days'),
            ('this_month', 'This Month'),
            ('custom', 'Custom Range'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if not val:
            return queryset
        
        now = timezone.now().date()
        if val == 'today':
            return queryset.filter(created_at__date=now)
        if val == 'yesterday':
            return queryset.filter(created_at__date=now - timedelta(days=1))
        if val == '7_days':
            return queryset.filter(created_at__date__gte=now - timedelta(days=7))
        if val == '30_days':
            return queryset.filter(created_at__date__gte=now - timedelta(days=30))
        if val == 'this_month':
            return queryset.filter(created_at__year=now.year, created_at__month=now.month)
        
        # 'custom' logic is handled by setting the fields in JS
        # Django handles the 'created_at__gte' and 'created_at__lte' params automatically 
        # in the URL if they are set correctly.
        return queryset


# ─── Customer Order ────────────────────────────────────────────────────────────

@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display  = (
        'order_number', 
        'user',               # ← Added User connection
        'is_guest',           # ← Added Guest flag
        'customer_tag',       # ← Added Customer Tag Badge
        'customer_name', 
        'email', 
        'phone',
        'payment_method_badge', 
        'payment_status_badge',
        'status',              # This is the editable dropdown (colored via JS/CSS)
        'items_count', 
        'total_display',
        'created_at',
    )
    list_editable = ('status',) 
    list_filter   = (
        'status', 
        'payment_method', 
        'payment_status', 
        'country', 
        CreatedAtRangeFilter,
    )
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'id')
    readonly_fields = (
        'order_number', 'created_at', 'updated_at',
        'items_total_display',
        'customer_order_tag', 
        'resend_notification_button',
    )
    inlines = [CustomerOrderItemInline, OrderStatusHistoryInline]

    # ── Customer Tag helpers ─────────────────────────────────────────────────

    def customer_tag(self, obj):
        rank = get_order_rank(obj)
        if rank == 1:
            return _badge("New", "#28a745")
        return _badge(f"Repeat {rank}", "#007bff")
    customer_tag.short_description = "Loyalty"

    def customer_order_tag(self, obj):
        rank = get_order_rank(obj)
        label = "First Time Order" if rank == 1 else f"Returning Customer (Order #{rank})"
        badge = self.customer_tag(obj)
        return format_html('{} <span style="margin-left:10px;font-size:13px;color:#666;">{}</span>', badge, label)

    customer_order_tag.short_description = "Loyalty Status"

    # ── List display helpers ─────────────────────────────────────────────────

    def order_number(self, obj):
        if not obj.pk: return "#NEW"
        return format_html('<strong>#Demo-{}</strong>', f"{obj.pk:05d}")

    order_number.short_description = "Order #"
    order_number.admin_order_field = 'id'

    def customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    customer_name.short_description = "Customer"

    def payment_method_badge(self, obj):
        icon = PAYMENT_METHOD_ICONS.get(obj.payment_method, '💳')
        label = obj.get_payment_method_display()
        return format_html('<span style="font-size:13px;">{} {}</span>', icon, label)

    payment_method_badge.short_description = "Payment"

    def payment_status_badge(self, obj):
        color = PAYMENT_STATUS_COLORS.get(obj.payment_status, '#888')
        return _badge(obj.get_payment_status_display(), color)
    payment_status_badge.short_description = "Payment Status"

    def order_status_badge(self, obj):
        color = ORDER_STATUS_COLORS.get(obj.status, '#888')
        return _badge(obj.get_status_display(), color)
    order_status_badge.short_description = "Order Status"

    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = "Items"

    def total_display(self, obj):
        return format_html('<strong>{} {}</strong>', obj.total_amount, settings.CURRENCY)

    total_display.short_description = "Total"

    def resend_notification_button(self, obj):
        if not obj.pk: return "-"
        from django.urls import reverse
        url = reverse('admin:resend-notification', args=[obj.pk])
        return format_html(
            '<div style="margin-top:5px;">'
            '<a class="button btn btn-primary" href="{}" style="padding:4px 12px; font-size:12px;">'
            '📨 Resend Notifications</a>'
            '</div>',
            url
        )

    resend_notification_button.short_description = "Notifications"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:order_id>/resend-notification/', 
                 self.admin_site.admin_view(self.resend_notification), 
                 name='resend-notification'),
            path('ajax/get-product-price/',
                 self.admin_site.admin_view(self.get_product_price),
                 name='ajax-get-product-price'),
        ]
        return custom_urls + urls

    def resend_notification(self, request, order_id):
        from .notifications import send_customer_notification
        from django.shortcuts import get_object_or_404, redirect
        order = get_object_or_404(CustomerOrder, pk=order_id)
        send_customer_notification(order, is_automated=False)
        self.message_user(request, f"Notifications have been successfully resent for Order #Demo-{order_id:05d}.")
        return redirect('admin:orders_customerorder_change', order_id)

    def get_product_price(self, request):
        from django.http import JsonResponse
        from products.models import Product
        product_id = request.GET.get('product_id')
        if not product_id:
            return JsonResponse({'error': 'No product_id provided'}, status=400)
        
        try:
            product = Product.objects.get(id=product_id)
            price_info = product.get_best_price_info()
            
            sku = product.skus.first()
            shipping_charge = 0
            if sku:
                shipping_charge = 0 if sku.free_shipping else (sku.additional_shipping_charge or 0)

            return JsonResponse({
                'unit_price': float(price_info['final_price']),
                'shipping_charge': float(shipping_charge),
                'product_name': product.name
            })
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def items_total_display(self, obj):
        from django.utils.html import format_html_join
        items = obj.items.all()
        rows = format_html_join(
            '',
            '<tr><td style="padding:8px 10px;">{}</td>'
            '<td style="padding:8px 10px;text-align:center;">{}</td>'
            '<td style="padding:8px 10px;text-align:right;">{} {}</td>'
            '<td style="padding:8px 10px;text-align:right;">{} {}</td>'
            '<td style="padding:8px 10px;text-align:right;font-weight:700;">{} {}</td></tr>',
            ((i.product_name, i.quantity, i.regular_price, settings.CURRENCY, i.unit_price, settings.CURRENCY, i.total_price, settings.CURRENCY) for i in items)
        )
        return format_html(
            '<table style="width:100%; border-collapse:collapse; font-size:13px; border:1px solid #eee; border-radius:8px; overflow:hidden;">'
            '<thead><tr style="background:#f8fafc; border-bottom:1px solid #eee;">'
            '<th style="padding:10px; text-align:left;">Product</th>'
            '<th style="padding:10px; text-align:center;">Qty</th>'
            '<th style="padding:10px; text-align:right;">Regular</th>'
            '<th style="padding:10px; text-align:right;">Sale</th>'
            '<th style="padding:10px; text-align:right;">Subtotal</th></tr></thead>'
            '<tbody>{}</tbody>'
            '<tfoot>'
            '<tr style="background:#fafafa;"><td colspan="4" style="padding:10px; text-align:right; color:#64748b;">Items Subtotal</td>'
            '<td style="padding:10px; text-align:right; color:#64748b;">{} {}</td></tr>'
            '<tr style="background:#fafafa;"><td colspan="4" style="padding:10px; text-align:right; color:#64748b;">Shipping Details</td>'
            '<td style="padding:10px; text-align:right; color:#64748b;">{} {}</td></tr>'
            '<tr style="background:#f1f5f9; font-weight:700; font-size:15px;"><td colspan="4" style="padding:12px 10px; text-align:right;">Grand Total Amount</td>'
            '<td style="padding:12px 10px; text-align:right; color:#2563eb;">{} {}</td></tr>'
            '</tfoot>'
            '</table>',
            mark_safe(rows),
            sum(i.total_price for i in items), settings.CURRENCY,
            obj.shipping_amount, settings.CURRENCY,
            obj.total_amount, settings.CURRENCY
        )

    items_total_display.short_description = "Detailed Summary"

    # ── Fieldsets ────────────────────────────────────────────────────────────

    fieldsets = (
        ('Order Identification', {
            'fields': (('order_number', 'customer_order_tag'),),
        }),
        ('Customer Details', {
            'fields': (
                ('first_name', 'last_name'),
                ('email', 'phone'),
                ('department', 'user', 'is_guest'),
            ),
        }),
        ('Shipping Address', {
            'fields': (
                ('country', 'city'),
                'street',
                'comment',
            ),
        }),
        ('Payment & Financials', {
            'fields': (
                ('payment_method', 'payment_status'),
                ('shipping_amount', 'total_amount'),
            ),
        }),
        ('Order Processing', {
            'fields': (
                'status',
                'resend_notification_button',
                'admin_notes',
                ('created_at', 'updated_at'),
            ),
        }),
        ('Items Summary Board', {
            'fields': ('items_total_display',),
        }),
    )

    class Media:
        css = {'all': ('admin/css/admin_orders.css',)}
        js = ('admin/js/admin_orders.js',)
