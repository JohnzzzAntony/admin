from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage, Offer, Collection
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# ─── Resources for Import/Export ─────────────────────────────────────────────

class CategoryResource(resources.ModelResource):
    class Meta: model = Category

class ProductResource(resources.ModelResource):
    class Meta: model = Product

# ─── Inlines ─────────────────────────────────────────────────────────────────

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0
    fields = (('image', 'image_url'), ('order', 'preview'))
    readonly_fields = ('preview',)
    
    def preview(self, obj):
        if obj.get_image_url:
            return mark_safe(f'<img src="{obj.get_image_url}" width="60" style="border-radius:4px;"/>')
        return "-"

# ─── Main Model Admins ───────────────────────────────────────────────────────

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('preview', 'name', 'category', 'regular_price', 'sale_price', 'quantity', 'show_on_homepage', 'stock_status')
    list_editable = ('show_on_homepage',)
    
    def is_active_label(self, obj): return "-"
    is_active_label.short_description = "Status"
    search_fields = ('name', 'slug', 'sku_id')
    readonly_fields = ('preview', 'sku_id')
    inlines = [ProductImageInline]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        from django.contrib import messages
        messages.success(request, f'✅ Product "{obj.name}" has been successfully saved.')

    def delete_model(self, request, obj):
        name = obj.name
        super().delete_model(request, obj)
        from django.contrib import messages
        messages.error(request, f'🗑️ Product "{name}" has been removed.')

    def preview(self, obj):
        if obj.get_image_url:
            return mark_safe(f'<img src="{obj.get_image_url}" width="45" height="45" style="object-fit:cover; border-radius:50%; border:1px solid #ddd;"/>')
        return "-"

    def stock_status(self, obj):
        return "✅ In Stock" if obj.is_in_stock() else "❌ Out of Stock"
    stock_status.short_description = "Stock"

    fieldsets = (
        ('Overview', {
            'fields': (('name', 'category'), ('slug', 'sku_id'), ('quantity', 'show_on_homepage')),
            'description': 'Core identity and stock availability.'
        }),
        ('Pricing & Shipping', {
            'fields': (('regular_price', 'sale_price'), ('shipping_status', 'delivery_time'), ('free_shipping', 'additional_shipping_charge')),
            'classes': ('collapse',),
        }),
        ('Dimensions & Weight', {
            'fields': (('weight', 'unit'), ('length', 'width', 'height')),
            'classes': ('collapse',),
        }),
        ('Detailed Content', {
            'fields': ('overview', 'features', 'technical_info'),
        }),
        ('Media Assets', {
            'fields': (('image', 'image_url'), ('brochure', 'preview')),
        }),
        ('Search Optimization', {
            'fields': (
                ('meta_title', 'meta_title_ar'), 
                ('meta_description', 'meta_description_ar'), 
                ('meta_keywords', 'meta_keywords_ar')
            ),
            'classes': ('collapse',),
        }),
    )
    radio_fields = {
        "shipping_status": admin.HORIZONTAL,
        "free_shipping": admin.HORIZONTAL,
        "show_on_homepage": admin.HORIZONTAL,
    }

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('name', 'parent', 'show_on_homepage', 'homepage_order')
    list_editable = ('show_on_homepage', 'homepage_order')
    list_filter = ('parent', 'show_on_homepage')
    search_fields = ('name', 'slug')
    autocomplete_fields = ('parent',)
    readonly_fields = ()
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        from django.contrib import messages
        messages.success(request, f'📂 Category "{obj.name}" has been saved.')

    def delete_model(self, request, obj):
        name = obj.name
        super().delete_model(request, obj)
        from django.contrib import messages
        messages.error(request, f'🗑️ Category "{name}" was removed.')

    fieldsets = (
        ('Hierarchy & Branding', {
            'fields': (
                ('name', 'parent'), 
                ('slug', 'homepage_order'), 
                'show_on_homepage',
                'description'
            ),
        }),
        ('Media & Icons', {
            'fields': (('image', 'image_url'), 'icon_svg'),
        }),
        ('Search Optimization', {
            'fields': (
                ('meta_title', 'meta_title_ar'), 
                ('meta_description', 'meta_description_ar'), 
                ('meta_keywords', 'meta_keywords_ar')
            ),
            'classes': ('collapse',),
        }),
    )
    radio_fields = {
        "show_on_homepage": admin.HORIZONTAL,
    }

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'offer_type', 'discount_value', 'start_date', 'end_date')
    list_filter = ('offer_type',)
    search_fields = ('name',)
    filter_horizontal = ('products',)

    fieldsets = (
        ('Offer Basics', {
            'fields': ('name', 'offer_type', 'discount_value')
        }),
        ('Active Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Apply to Products', {
            'fields': ('products',),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        from django.contrib import messages
        messages.success(request, f'🏷️ Offer "{obj.name}" has been saved.')

    def delete_model(self, request, obj):
        name = obj.name
        super().delete_model(request, obj)
        from django.contrib import messages
        messages.error(request, f'🗑️ Offer "{name}" was removed.')

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    list_editable = ('display_order',)
    filter_horizontal = ('products',)
    radio_fields = {}
    
    fieldsets = (
        ('Collection Info', {
            'fields': (('name', 'slug'), ('display_order')),
        }),
        ('Branding', {
            'fields': (('banner', 'banner_url'),),
        }),
        ('Products', {
            'fields': ('products',),
            'description': 'Manage items belonging to this specific collection.'
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        from django.contrib import messages
        messages.success(request, f'📦 Collection "{obj.name}" has been saved.')

    def delete_model(self, request, obj):
        name = obj.name
        super().delete_model(request, obj)
        from django.contrib import messages
        messages.error(request, f'🗑️ Collection "{name}" was removed.')

