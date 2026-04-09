from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Product, Category
from .serializers import ProductSearchSerializer, CategorySerializer

class ProductSearchAPIView(APIView):
    """
    Consolidated search API for products and categories.
    Used by the dynamic header component.
    """
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query or len(query) < 2:
            return Response({'products': [], 'categories': []})
        
        # 1. Search Products
        products = Product.objects.filter(
            is_active=True
        ).filter(
            Q(name__icontains=query) | 
            Q(category__name__icontains=query) |
            Q(meta_keywords__icontains=query)
        ).distinct()[:10]
        
        # 2. Search Categories
        categories = Category.objects.filter(
            is_active=True
        ).filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).distinct()[:5]
        
        return Response({
            'products': ProductSearchSerializer(products, many=True).data,
            'categories': CategorySerializer(categories, many=True).data,
        })
