from rest_framework import serializers
from .models import Category, Product

class CategoryTreeSerializer(serializers.ModelSerializer):
    """
    Returns a recursive nested tree of active categories.
    """
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'image', 
            'image_url', 'is_active', 'created_at', 'updated_at', 
            'children'
        ]

    def get_children(self, obj):
        # Optimized recursive fetch for children
        children = obj.subcategories.filter(is_active=True).order_by('name')
        return CategoryTreeSerializer(children, many=True).data

class CategoryDetailSerializer(serializers.ModelSerializer):
    """
    Standard serializer for individual category operations.
    """
    class Meta:
        model = Category
        fields = '__all__'

class CategoryMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryMinimalSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'image', 'image_url', 'is_active']
