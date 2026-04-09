from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image_url', 'icon_svg', 'subcategories', 'homepage_order')

    def get_subcategories(self, obj):
        # Recursively serialize subcategories
        subs = obj.subcategories.all().order_by('homepage_order', 'name')
        return CategorySerializer(subs, many=True).data
    
    def get_image_url(self, obj):
        return obj.get_image_url

# Alias or specialized tree serializer for hierarchical UI
class CategoryTreeSerializer(CategorySerializer):
    """Specifically used for building the primary navigation tree."""
    pass

class CategoryDetailSerializer(serializers.ModelSerializer):
    """Detailed view for a single category, including parent info."""
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug', 'description', 'image_url', 
            'icon_svg', 'parent', 'parent_name', 'seo_meta_data'
        )

    def get_image_url(self, obj):
        return obj.get_image_url

class ProductListSerializer(serializers.ModelSerializer):
    """Simplified product listing for category-based results."""
    image_url = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'image_url', 'category_name', 'regular_price', 'sale_price')

    def get_image_url(self, obj):
        # Use existing image logic from model
        return obj.get_image_url if hasattr(obj, 'get_image_url') else None

class ProductSearchSerializer(ProductListSerializer):
    """Search results with additional context if needed."""
    pass
