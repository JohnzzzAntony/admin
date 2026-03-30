from django.contrib import admin
from django.utils.html import mark_safe
from .models import Category, Product, ProductSKU, ProductImage, Attribute, AttributeOption, ProductAttributeValue


# ─── Inlines ─────────────────────────────────────────────────────────────────

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'image_url', 'order')


class SKUInline(admin.StackedInline):
    model = ProductSKU
    extra = 0
    verbose_name = "Product Variant / SKU"
    verbose_name_plural = "Product Variants / SKUs"
    fieldsets = (
        (None, {
            'fields': (
                ('sku_id', 'title'),
                ('quantity', 'unit'),
                ('weight', 'length'),
                ('width', 'height'),
                ('shipping_status', 'delivery_time'),
                ('free_shipping', 'additional_shipping_charge'),
            )
        }),
    )


class AttributeOptionInline(admin.TabularInline):
    model = AttributeOption
    extra = 3


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 3
    verbose_name = "Characteristic"
    verbose_name_plural = "Product Characteristics"


# ─── Attribute ────────────────────────────────────────────────────────────────

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'field_type')
    inlines = [AttributeOptionInline]


# ─── Product ─────────────────────────────────────────────────────────────────

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'stock_status')
    search_fields = ('name', 'meta_title', 'meta_keywords')
    readonly_fields = ('slug', 'product_seo_std_heading', 'product_seo_en_heading', 'product_seo_ar_heading')
    inlines = [ProductImageInline, ProductAttributeValueInline, SKUInline]

    def stock_status(self, obj):
        return "✅ In Stock" if obj.is_in_stock() else "❌ Out of Stock"
    stock_status.short_description = "Stock"

    def product_seo_std_heading(self, obj):
        return mark_safe(
            '<p style="margin:12px 0 4px;font-weight:700;font-size:13px;'
            'color:#2271b1;border-bottom:2px solid #2271b1;padding-bottom:4px;">'
            '🌐 Standard (Default)</p>'
        )
    product_seo_std_heading.short_description = ''

    def product_seo_en_heading(self, obj):
        return mark_safe(
            '<p style="margin:20px 0 4px;font-weight:700;font-size:13px;'
            'color:#1d6fa4;border-bottom:2px solid #1d6fa4;padding-bottom:4px;">'
            '🇬🇧 English (EN)</p>'
        )
    product_seo_en_heading.short_description = ''

    def product_seo_ar_heading(self, obj):
        return mark_safe(
            '<p style="margin:20px 0 4px;font-weight:700;font-size:13px;'
            'color:#8b5e3c;border-bottom:2px solid #8b5e3c;padding-bottom:4px;">'
            '🇸🇦 Arabic (AR)</p>'
        )
    product_seo_ar_heading.short_description = ''

    fieldsets = (
        ('Product Identification', {
            'fields': (('category', 'name'), 'slug'),
        }),
        ('Pricing & Availability', {
            'fields': (('regular_price', 'sale_price'), 'is_active'),
        }),
        ('Media & Files', {
            'fields': (('image', 'image_url'), 'brochure'),
        }),
        ('Detailed Content', {
            'fields': ('features', 'overview', 'technical_info'),
        }),
        ('Search Engines (SEO)', {
            'fields': (
                'product_seo_std_heading',
                'meta_title', 'meta_description', 'meta_keywords', 'url_alias',
                'product_seo_en_heading',
                'meta_title_en', 'meta_description_en', 'meta_keywords_en', 'url_alias_en',
                'product_seo_ar_heading',
                'meta_title_ar', 'meta_description_ar', 'meta_keywords_ar', 'url_alias_ar',
            ),
        }),
    )


# ─── Category ────────────────────────────────────────────────────────────────

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    list_filter = ('parent',)
    filter_horizontal = ('attributes',)
    readonly_fields = ('slug', 'cat_seo_std_heading', 'cat_seo_en_heading', 'cat_seo_ar_heading')

    def cat_seo_std_heading(self, obj):
        return mark_safe(
            '<p style="margin:12px 0 4px;font-weight:700;font-size:13px;'
            'color:#2271b1;border-bottom:2px solid #2271b1;padding-bottom:4px;">'
            '🌐 Standard (Default)</p>'
        )
    cat_seo_std_heading.short_description = ''

    def cat_seo_en_heading(self, obj):
        return mark_safe(
            '<p style="margin:20px 0 4px;font-weight:700;font-size:13px;'
            'color:#1d6fa4;border-bottom:2px solid #1d6fa4;padding-bottom:4px;">'
            '🇬🇧 English (EN)</p>'
        )
    cat_seo_en_heading.short_description = ''

    def cat_seo_ar_heading(self, obj):
        return mark_safe(
            '<p style="margin:20px 0 4px;font-weight:700;font-size:13px;'
            'color:#8b5e3c;border-bottom:2px solid #8b5e3c;padding-bottom:4px;">'
            '🇸🇦 Arabic (AR)</p>'
        )
    cat_seo_ar_heading.short_description = ''

    fieldsets = (
        ('Category Details', {
            'fields': ('parent', 'name', 'slug'),
        }),
        ('Image', {
            'fields': (('image', 'image_url'),),
        }),
        ('Attributes', {
            'fields': ('attributes',),
        }),
        ('Search Engines (SEO)', {
            'fields': (
                'cat_seo_std_heading',
                'meta_title', 'meta_description', 'meta_keywords', 'url_alias',
                'cat_seo_en_heading',
                'meta_title_en', 'meta_description_en', 'meta_keywords_en', 'url_alias_en',
                'cat_seo_ar_heading',
                'meta_title_ar', 'meta_description_ar', 'meta_keywords_ar', 'url_alias_ar',
            ),
        }),
    )
