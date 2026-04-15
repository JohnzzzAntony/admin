from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import Product, Category, ProductImage, Wishlist, Brand, Collection

@staff_member_required
def delete_product_media(request, pk):
    """Instantly deletes a ProductImage and its physical file via AJAX."""
    if request.method == 'POST':
        try:
            image_obj = get_object_or_404(ProductImage, pk=pk)
            if image_obj.image:
                image_obj.image.delete(save=False)
            image_obj.delete()
            return JsonResponse({'status': 'success', 'message': 'Gallery image deleted permanently.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'POST required'}, status=405)

@staff_member_required
def clear_primary_product_image(request, pk):
    """Instantly clears the main image field of a Product via AJAX."""
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, pk=pk)
            if product.image:
                # Use storage delete to ensure Cloudinary/S3 file is removed
                product.image.delete(save=False)
                product.image = None
                product.save(update_fields=['image'])
            return JsonResponse({'status': 'success', 'message': 'Primary image cleared permanently.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'POST required'}, status=405)

@login_required
def wishlist_view(request):
    """Displays the user's favorited products."""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product').prefetch_related(
        'product__offers', 'product__images', 'product__category'
    ).order_by('-added_at')
    
    products = [item.product for item in wishlist_items]
    
    return render(request, 'products/wishlist.html', {
        'products': products
    })

@login_required
def toggle_wishlist(request, product_id):
    """Toggles a product in the user's wishlist via AJAX."""
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, pk=product_id)
            wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
            
            if not created:
                wishlist_item.delete()
                # Get updated count
                count = Wishlist.objects.filter(user=request.user).count()
                return JsonResponse({'status': 'removed', 'count': count, 'message': 'Removed from wishlist.'})
            
            count = Wishlist.objects.filter(user=request.user).count()
            return JsonResponse({'status': 'added', 'id': product.id, 'count': count, 'message': 'Added to wishlist!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'POST required'}, status=405)

@staff_member_required
def get_subcategories(request, parent_id):
    """Returns a list of subcategories for a given parent ID as JSON."""
    subcategories = Category.objects.filter(parent_id=parent_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def category_index(request):
    """Shows top-level categories in a professional grid."""
    categories = Category.objects.filter(parent__isnull=True, is_active=True)
    if not categories.exists():
        categories = Category.objects.filter(is_active=True)
    return render(request, 'products/category_index.html', {'categories': categories})

def product_list(request):
    """Shows all products with stock, and categories in sidebar."""
    parents = Category.objects.filter(parent__isnull=True, is_active=True)
    categories = parents if parents.count() > 1 else Category.objects.filter(is_active=True)

    # Only show active, in-stock products
    products = Product.objects.filter(
        is_active=True,
        quantity__gt=0,
        shipping_status='available'
    ).select_related('category').prefetch_related(
        'offers',
        'images'
    ).distinct().order_by('-id')
    
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(overview__icontains=query) | Q(sku_id__icontains=query)
        )
    
    return render(request, 'products/product_list.html', {
        'categories': categories,
        'products': products
    })

def category_detail(request, slug=None, hierarchy_path=None):
    """
    Highly advanced SEO-friendly category view that supports absolute paths.
    """
    if hierarchy_path:
        slug = hierarchy_path.strip('/').split('/')[-1]
    
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    all_categories_in_branch = category.get_all_children(include_self=True)
    cat_ids = [c.id for c in all_categories_in_branch]

    products = Product.objects.filter(
        category_id__in=cat_ids,
        is_active=True,
        quantity__gt=0,
        shipping_status='available'
    ).select_related('category').prefetch_related(
        'offers',
        'images'
    ).distinct().order_by('-id')
    
    # Root categories for sidebar
    roots = Category.objects.filter(parent__isnull=True, is_active=True).prefetch_related('subcategories')

    return render(request, 'products/product_list.html', {
        'current_category': category, 
        'products': products,
        'categories': roots,
        'ancestors': category.get_ancestors()
    })



from core.design_models import DesignSettings

def product_detail(request, slug=None, pk=None):
    """SEO-friendly product detail page. Supports both slug and PK for administrative legacy tools."""
    if pk:
        product = get_object_or_404(
            Product.objects.select_related('category').prefetch_related('offers', 'images'), 
            pk=pk, is_active=True
        )
    else:
        product = get_object_or_404(
            Product.objects.select_related('category').prefetch_related('offers', 'images'), 
            slug=slug, is_active=True
        )

    # Fetch related products from the same category
    design = DesignSettings.objects.first()
    related_count = design.pd_related_count if design else 4
    
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True,
        quantity__gt=0
    ).exclude(id=product.id).select_related('category').prefetch_related('offers', 'images')[:related_count]

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products
    })


# ── REST API For Category Management ───────────────────────────────────────────
try:
    from rest_framework import viewsets, permissions, status
    from rest_framework.response import Response
    from rest_framework.decorators import action
    from .serializers import CategoryTreeSerializer, CategoryDetailSerializer
    _DRF_AVAILABLE = True
except ImportError:
    _DRF_AVAILABLE = False

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
        roots = self.get_queryset().filter(parent__isnull=True)
        serializer = CategoryTreeSerializer(roots, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='products')
    def get_products(self, request, slug=None):
        """Returns products specifically for this category and all its subcategories."""
        category = self.get_object()
        all_cat_ids = [c.id for c in category.get_all_children(include_self=True)]
        
        from .serializers import ProductListSerializer 
        products = Product.objects.filter(category_id__in=all_cat_ids)
        return Response(ProductListSerializer(products, many=True).data)

    def destroy(self, request, *args, **kwargs):
        """Handle children properly - logic is in on_delete=CASCADE in models.py"""
        return super().destroy(request, *args, **kwargs)

def collection_detail(request, slug):
    """
    Shows products belonging to a specific collection.
    """
    collection = get_object_or_404(Collection, slug=slug, is_active=True)
    products = collection.products.filter(
        is_active=True,
        quantity__gt=0,
        shipping_status='available'
    ).select_related('category').prefetch_related(
        'offers',
        'images'
    ).distinct().order_by('-id')
    
    # Root categories for sidebar
    roots = Category.objects.filter(parent__isnull=True, is_active=True).prefetch_related('subcategories')

    return render(request, 'products/product_list.html', {
        'collection': collection, 
        'products': products,
        'categories': roots,
        'title': collection.name
    })

def brand_list(request):
    """Shows all active brands."""
    brands = Brand.objects.filter(is_active=True)
    return render(request, 'products/brand_list.html', {'brands': brands})

def brand_detail(request, slug):
    """Shows products for a specific brand."""
    brand = get_object_or_404(Brand, slug=slug, is_active=True)
    products = Product.objects.filter(
        brand=brand,
        is_active=True,
        quantity__gt=0,
        shipping_status='available'
    ).select_related('category', 'brand').prefetch_related(
        'offers',
        'images'
    ).distinct().order_by('-id')
    
    roots = Category.objects.filter(parent__isnull=True, is_active=True).prefetch_related('subcategories')
    
    return render(request, 'products/product_list.html', {
        'current_brand': brand,
        'products': products,
        'categories': roots,
        'title': f"Products by {brand.name}"
    })

