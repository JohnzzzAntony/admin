from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Product, Category

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
    gallery_image_urls = fields.Field(column_name='gallery_image_urls')
    category_image_url = fields.Field(column_name='category_image_url')

    class Meta:
        model = Product
        import_id_fields = ('name',)
        # All fields are now on Product (Flattened model)
        fields = (
            'id', 'category', 'name', 'slug', 'image_url', 'features', 
            'overview', 'technical_info', 'regular_price', 'sale_price',
            'meta_title', 'meta_title_ar', 'meta_description', 'meta_description_ar', 
            'meta_keywords', 'meta_keywords_ar',
            'sku_id', 'quantity', 'shipping_status', 'weight', 
            'length', 'width', 'height', 'delivery_time',
            'free_shipping', 'additional_shipping_charge',
            'gallery_image_urls', 'category_image_url'
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
            
        # 1. Handle Gallery Images (multiple URLs comma separated)
        gallery_urls = row.get('gallery_image_urls')
        if gallery_urls:
            from .models import ProductImage
            url_list = [u.strip() for u in gallery_urls.split(',') if u.strip()]
            for url in url_list:
                ProductImage.objects.get_or_create(product=instance, image_url=url)
