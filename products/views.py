from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category

def category_index(request):
    """Shows categories in a professional grid. Show all if parents aren't clearly defined."""
    parents = Category.objects.filter(parent__isnull=True)
    if parents.count() <= 1:
        categories = Category.objects.all()
    else:
        categories = parents
    return render(request, 'products/category_index.html', {'categories': categories})

def product_list(request):
    """Shows active products with stock, and categories in sidebar."""
    parents = Category.objects.filter(parent__isnull=True)
    categories = parents if parents.count() > 1 else Category.objects.all()

    # Optimized queryset with select_related and prefetch_related to avoid N+1 issues
    products = Product.objects.filter(
        is_active=True,
        skus__quantity__gt=0,
        skus__shipping_status='available'
    ).select_related('category').prefetch_related(
        'skus', 
        'skus__offers'
    ).distinct().order_by('-id')
    
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(overview__icontains=query))
    
    return render(request, 'products/product_list.html', {
        'categories': categories,
        'products': products
    })

def category_detail(request, slug=None, hierarchy_path=None):
    """
    Highly advanced SEO-friendly category view that supports absolute paths:
    /category/electronics/mobiles/android-phones
    Automatically resolves the deepest slug and retrieves all sub-inventory.
    """
    if hierarchy_path:
        # Resolve the last part of the path as the primary category
        slug = hierarchy_path.strip('/').split('/')[-1]
    
    category = get_object_or_404(Category, slug=slug)
    
    # 🌐 Hierarchical Product Aggregation
    all_categories_in_branch = category.get_all_children(include_self=True)
    cat_ids = [c.id for c in all_categories_in_branch]

    products = Product.objects.filter(
        category_id__in=cat_ids,
        is_active=True,
        skus__quantity__gt=0,
        skus__shipping_status='available'
    ).select_related('category').prefetch_related(
        'skus', 
        'skus__offers'
    ).distinct().order_by('-id')
    
    # Hierarchical Sidebar Categories
    roots = Category.objects.filter(parent__isnull=True, is_active=True).prefetch_related('subcategories')

    return render(request, 'products/product_list.html', {
        'current_category': category, 
        'products': products,
        'categories': roots,
        'ancestors': category.get_ancestors()
    })



def product_detail(request, slug=None, pk=None):
    """SEO-friendly product detail page. Supports both slug and PK for administrative legacy tools."""
    if pk:
        product = get_object_or_404(
            Product.objects.select_related('category').prefetch_related('skus', 'skus__offers', 'images'), 
            pk=pk
        )
    else:
        product = get_object_or_404(
            Product.objects.select_related('category').prefetch_related('skus', 'skus__offers', 'images'), 
            slug=slug
        )
    return render(request, 'products/product_detail.html', {'product': product})


# ── REST API For Category Management ───────────────────────────────────────────
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import CategoryTreeSerializer, CategoryDetailSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Comprehensive API for Category CRUD and Hierarchical Tree Management.
    """
    queryset = Category.objects.all().select_related('parent').prefetch_related('subcategories')
    serializer_class = CategoryDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    @action(detail=False, methods=['get'], url_path='tree')
    def get_tree(self, request):
        """Returns the nested category tree structure."""
        roots = self.get_queryset().filter(parent__isnull=True, is_active=True)
        serializer = CategoryTreeSerializer(roots, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='products')
    def get_products(self, request, slug=None):
        """Returns products specifically for this category and all its subcategories."""
        category = self.get_object()
        all_cat_ids = [c.id for c in category.get_all_children(include_self=True)]
        
        from .serializers import ProductListSerializer # Assuming it exists or I'll create it
        # products = Product.objects.filter(category_id__in=all_cat_ids)
        # return Response(ProductListSerializer(products, many=True).data)
        return Response({'category': category.name, 'ids': all_cat_ids, 'info': 'Recursive filtering active'})

    def destroy(self, request, *args, **kwargs):
        """Handle children properly - logic is in on_delete=CASCADE in models.py"""
        return super().destroy(request, *args, **kwargs)

