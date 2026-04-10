from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage, Offer, Collection
from .forms import ProductAdminForm
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
        url = obj.get_image_url() if hasattr(obj, 'get_image_url') else None
        if url:
            return mark_safe(f'<img src="{url}" width="60" style="border-radius:4px;"/>')
        return "-"

class SubCategoryInline(admin.TabularInline):
    model = Category
    fk_name = 'parent'
    extra = 0
    verbose_name = "Sub Category"
    verbose_name_plural = "Sub Categories"
    fields = ('name', 'slug', 'show_on_homepage', 'homepage_order')
    prepopulated_fields = {"slug": ("name",)}

# ─── Main Model Admins ───────────────────────────────────────────────────────

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    form = ProductAdminForm
    resource_class = ProductResource
    list_display = ('preview', 'name', 'category_display', 'regular_price', 'sale_price', 'quantity', 'show_on_homepage', 'stock_status')
    list_editable = ('show_on_homepage',)
    search_fields = ('name', 'slug', 'sku_id')
    readonly_fields = ('preview', 'sku_id')
    inlines = [ProductImageInline]

    class Media:
        js = ('admin/js/dynamic_categories.js',)

    def preview(self, obj):
        if obj.get_image_url:
            return mark_safe(f'<img src="{obj.get_image_url}" width="45" height="45" style="object-fit:cover; border-radius:50%; border:1px solid #ddd;"/>')
        return "-"

    def category_display(self, obj):
        if not obj.category: return "-"
        if obj.category.parent:
            return mark_safe(f'<span style="color:#666; font-size:0.85em;">{obj.category.parent.name}</span><br><b>{obj.category.name}</b>')
        return obj.category.name
    category_display.short_description = "Category"

    def parent_category(self, obj):
        return obj.category.parent if obj.category and obj.category.parent else (obj.category if obj.category else "-")
    parent_category.short_description = "Parent Category"

    def stock_status(self, obj):
        return "✅ In Stock" if obj.is_in_stock() else "❌ Out of Stock"
    stock_status.short_description = "Stock"

    fieldsets = (
        ('Overview', {
            'fields': (
                ('name', 'sku_id'), 
                ('parent_category', 'category'),
                ('slug', 'quantity'),
                'show_on_homepage'
            ),
            'description': 'Core identity and stock availability. Choose a parent category to see subcategories.'
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
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
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
    list_display = ('name', 'show_on_homepage', 'homepage_order')
    list_editable = ('show_on_homepage', 'homepage_order')
    list_filter = ('show_on_homepage',)
    search_fields = ('name', 'slug')
    autocomplete_fields = ('parent',)
    inlines = [SubCategoryInline]
    prepopulated_fields = {"slug": ("name",)}
    
    def get_queryset(self, request):
        """Only show root categories in the main list."""
        qs = super().get_queryset(request)
        return qs.filter(parent__isnull=True)
    
    fieldsets = (
        ('Hierarchy & Branding', {
            'fields': (
                ('name', 'parent'), 
                ('slug', 'homepage_order'), 
                ('image', 'image_url'),
                'icon_svg',
                'show_on_homepage',
                'description'
            )
        }),
        ('Search Optimization', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',),
        }),
    )
    radio_fields = {
        "show_on_homepage": admin.HORIZONTAL,
    }

    class Media:
        css = {
            'all': ('admin/css/subcategory_admin.css',)
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

