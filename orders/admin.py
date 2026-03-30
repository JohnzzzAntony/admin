from django.contrib import admin
from django.utils.html import mark_safe
from django.db.models import Q
from .models import CustomerOrder, CustomerOrderItem


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
    'pending':    '#ffc107',
    'confirmed':  '#17a2b8',
    'processing': '#007bff',
    'shipped':    '#6f42c1',
    'delivered':  '#28a745',
    'cancelled':  '#dc3545',
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
    fields = ('product', 'product_name', 'quantity', 'unit_price', 'total_price')

    def has_add_permission(self, request, obj=None):
        return True


# ─── Customer Order ────────────────────────────────────────────────────────────

@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display  = (
        'order_number', 
        'customer_tag',       # ← Added Customer Tag Badge
        'customer_name', 
        'email', 
        'phone',
        'payment_method_badge', 
        'payment_status_badge',
        'order_status_badge', 
        'items_count', 
        'total_display',
        'created_at',
    )
    list_filter   = ('status', 'payment_method', 'payment_status', 'country', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'id')
    readonly_fields = (
        'order_number', 'created_at', 'updated_at',
        'order_summary_heading', 'billing_heading',
        'payment_heading', 'management_heading',
        'items_total_display',
        'customer_order_tag',  # ← Added detailed badge for detail page
    )
    inlines = [CustomerOrderItemInline]

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
        return mark_safe(f'{badge} <span style="margin-left:10px;font-size:13px;color:#666;">{label}</span>')
    customer_order_tag.short_description = "Customer Loyalty Status"

    # ── List display helpers ─────────────────────────────────────────────────

    def order_number(self, obj):
        return mark_safe(f'<strong>#JKR-{obj.pk:05d}</strong>')
    order_number.short_description = "Order #"
    order_number.admin_order_field = 'id'

    def customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    customer_name.short_description = "Customer"

    def payment_method_badge(self, obj):
        icon = PAYMENT_METHOD_ICONS.get(obj.payment_method, '💳')
        label = obj.get_payment_method_display()
        return mark_safe(f'<span style="font-size:13px;">{icon} {label}</span>')
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
        return mark_safe(f'<strong>{obj.total_amount} AED</strong>')
    total_display.short_description = "Total"

    # ── Detail page readonly section headings (styled separators) ───────────

    def order_summary_heading(self, obj):
        return mark_safe(
            f'<div style="background:#f0f6ff;border-left:4px solid #2271b1;padding:10px 16px;border-radius:0 8px 8px 0;margin:8px 0;">'
            f'<strong style="color:#2271b1;font-size:13px;">📋 Order #JKR-{obj.pk:05d} &nbsp;|&nbsp; '
            f'Placed: {obj.created_at.strftime("%d %b %Y, %H:%M")}</strong></div>'
        )
    order_summary_heading.short_description = ''

    def billing_heading(self, obj):
        return mark_safe('<p style="margin:16px 0 4px;font-weight:700;font-size:13px;color:#2271b1;border-bottom:2px solid #2271b1;padding-bottom:4px;">🏠 Billing & Customer Details</p>')
    billing_heading.short_description = ''

    def payment_heading(self, obj):
        return mark_safe('<p style="margin:16px 0 4px;font-weight:700;font-size:13px;color:#1d6fa4;border-bottom:2px solid #1d6fa4;padding-bottom:4px;">💳 Payment Information</p>')
    payment_heading.short_description = ''

    def management_heading(self, obj):
        return mark_safe('<p style="margin:16px 0 4px;font-weight:700;font-size:13px;color:#1a7a4a;border-bottom:2px solid #1a7a4a;padding-bottom:4px;">⚙️ Order Management</p>')
    management_heading.short_description = ''

    def items_total_display(self, obj):
        total = sum(i.total_price for i in obj.items.all())
        rows = "".join(
            f'<tr><td style="padding:4px 10px;">{i.product_name}</td>'
            f'<td style="padding:4px 10px;text-align:center;">{i.quantity}</td>'
            f'<td style="padding:4px 10px;text-align:right;">{i.unit_price} AED</td>'
            f'<td style="padding:4px 10px;text-align:right;font-weight:700;">{i.total_price} AED</td></tr>'
            for i in obj.items.all()
        )
        return mark_safe(
            f'<table style="width:100%;border-collapse:collapse;font-size:13px;">'
            f'<thead><tr style="background:#f5f5f5;">'
            f'<th style="padding:6px 10px;text-align:left;">Product</th>'
            f'<th style="padding:6px 10px;text-align:center;">Qty</th>'
            f'<th style="padding:6px 10px;text-align:right;">Unit Price</th>'
            f'<th style="padding:6px 10px;text-align:right;">Total</th></tr></thead>'
            f'<tbody>{rows}</tbody>'
            f'<tfoot><tr><td colspan="3" style="padding:8px 10px;font-weight:700;text-align:right;">Grand Total</td>'
            f'<td style="padding:8px 10px;font-weight:700;text-align:right;color:#2271b1;">{total} AED</td></tr></tfoot>'
            f'</table>'
        )
    items_total_display.short_description = "Items Summary"

    # ── Fieldsets ────────────────────────────────────────────────────────────

    fieldsets = (
        ('Order Overview', {
            'fields': ('order_summary_heading',),
        }),
        ('Customer Status', {
            'fields': ('customer_order_tag',),
        }),
        ('Billing & Customer Details', {
            'fields': (
                'billing_heading',
                ('first_name', 'last_name'),
                ('email', 'phone'),
                'department',
                ('country', 'city'),
                'street',
                'comment',
            ),
        }),
        ('Payment', {
            'fields': (
                'payment_heading',
                ('payment_method', 'payment_status'),
            ),
        }),
        ('Order Management', {
            'fields': (
                'management_heading',
                ('status', 'total_amount'),
                'admin_notes',
                ('created_at', 'updated_at'),
            ),
        }),
        ('Items Summary', {
            'fields': ('items_total_display',),
        }),
    )

    class Media:
        css = {'all': ('admin/css/custom_order.css',)}
