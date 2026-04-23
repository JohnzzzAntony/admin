from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Product, Category, Brand

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
    brand = fields.Field(
        column_name='brand',
        attribute='brand',
        widget=ForeignKeyWidget(Brand, 'name')
    )
    # Unified import helper fields
    gallery_image_urls = fields.Field(column_name='gallery_image_urls')
    category_image_url = fields.Field(column_name='category_image_url')

    class Meta:
        model = Product
        import_id_fields = ('name',)
        # Comprehensive list of fields for a full export/import cycle
        fields = (
            'id', 'category', 'brand', 'name', 'slug', 'image', 'image_url', 'sku_id', 'quantity', 'unit',
            'regular_price', 'sale_price', 'shipping_status', 'free_shipping', 
            'additional_shipping_charge', 'delivery_time', 'tax_percentage', 
            'weight', 'length', 'width', 'height', 'features', 'overview',
            'technical_info', 'shipping_returns', 'avg_rating', 'review_count', 'badge', 'badge_color',
            'is_featured', 'show_on_homepage', 'is_active', 'created_at',
            'meta_title', 'meta_description', 'meta_keywords',
            'gallery_image_urls', 'category_image_url'
        )
        export_order = fields

    def before_import_row(self, row, **kwargs):
        # 1. Create/Update Category automatically (Supports hierarchical paths like 'Parent > Child')
        category_name = row.get('category')
        cat_img_url = row.get('category_image_url')
        if category_name:
            category_name = str(category_name).strip()
            if " > " in category_name:
                # Resolve hierarchy: Parent > Child > Subchild
                parts = [p.strip() for p in category_name.split(" > ")]
                parent = None
                for part in parts:
                    cat, created = Category.objects.get_or_create(name=part, parent=parent)
                    parent = cat
                # Final category is the leaf
                final_cat = parent
            else:
                final_cat, created = Category.objects.get_or_create(name=category_name)
            
            if cat_img_url and final_cat:
                final_cat.image_url = cat_img_url
                final_cat.save()
            
            # Crucial: update the row value to just the leaf name so ForeignKeyWidget finds it
            row['category'] = final_cat.name

        # 2. Create/Update Brand automatically
        brand_name = row.get('brand')
        if brand_name:
            brand_name = str(brand_name).strip()
            if brand_name:
                Brand.objects.get_or_create(name=brand_name)

    def after_import_row(self, row, row_result, **kwargs):
        instance = row_result.instance
        if not instance or not instance.id:
            return 
            
        # Handle Gallery Images (multiple URLs comma separated)
        gallery_urls = row.get('gallery_image_urls')
        if gallery_urls:
            from .models import ProductImage
            url_list = [u.strip() for u in gallery_urls.split(',') if u.strip()]
            for url in url_list:
                ProductImage.objects.get_or_create(product=instance, image_url=url)
