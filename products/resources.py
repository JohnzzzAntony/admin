from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Product, Category, ProductSKU

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        import_id_fields = ('name',)
        fields = ('id', 'parent', 'name', 'slug', 'image_url', 'show_on_homepage', 'homepage_order')

class ProductResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')
    )
    # Unified import helper fields
    sku_title = fields.Field(column_name='sku_title')
    sku_id = fields.Field(column_name='sku_id')
    sku_quantity = fields.Field(column_name='sku_quantity')
    sku_shipping_status = fields.Field(column_name='sku_shipping_status')
    sku_weight = fields.Field(column_name='sku_weight')
    gallery_image_urls = fields.Field(column_name='gallery_image_urls')
    category_image_url = fields.Field(column_name='category_image_url')

    class Meta:
        model = Product
        import_id_fields = ('name',)
        fields = (
            'id', 'category', 'name', 'slug', 'image_url', 'features', 
            'overview', 'technical_info', 'regular_price', 'sale_price', 'is_active',
            'meta_title', 'meta_description', 'meta_keywords'
        )

    def before_import_row(self, row, **kwargs):
        # Create/Update category
        category_name = row.get('category')
        cat_img_url = row.get('category_image_url')
        if category_name:
            cat, created = Category.objects.get_or_create(name=category_name)
            if cat_img_url:
                cat.image_url = cat_img_url
                cat.save()

    def after_import_row(self, row, row_result, **kwargs):
        instance = row_result.instance
        if not instance or not instance.id:
            return 
            
        # 1. Handle SKU
        sku_id = row.get('sku_id')
        if not sku_id:
            sku_id = f"JKR-{instance.slug[:10].upper()}-BULK"

        sku, created = ProductSKU.objects.get_or_create(
            product=instance,
            sku_id=sku_id,
            defaults={
                'title': row.get('sku_title', 'Standard'),
                'quantity': row.get('sku_quantity', 0),
                'shipping_status': row.get('sku_shipping_status', 'available'),
                'weight': row.get('sku_weight', 0),
            }
        )
        if not created:
            sku.title = row.get('sku_title', sku.title)
            sku.quantity = row.get('sku_quantity', sku.quantity)
            sku.shipping_status = row.get('sku_shipping_status', sku.shipping_status)
            sku.save()

        # 2. Handle Gallery Images (multiple URLs comma separated)
        gallery_urls = row.get('gallery_image_urls')
        if gallery_urls:
            from .models import ProductImage
            url_list = [u.strip() for u in gallery_urls.split(',') if u.strip()]
            # Optional: Clear existing if you want a clean sync, but we'll just add
            for url in url_list:
                ProductImage.objects.get_or_create(product=instance, image_url=url)

class ProductSKUResource(resources.ModelResource):
    product = fields.Field(
        column_name='product',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'name')
    )

    class Meta:
        model = ProductSKU
        import_id_fields = ('sku_id',)
        fields = (
            'id', 'product', 'title', 'sku_id', 'quantity', 'unit', 
            'weight', 'length', 'width', 'height', 'delivery_time', 
            'shipping_status', 'free_shipping', 'additional_shipping_charge'
        )
