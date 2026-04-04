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

def category_detail(request, slug):
    """Shows in-stock products within a category and its subcategories."""
    category = get_object_or_404(Category, slug=slug)
    # Get products from current category or children, only if they have stock
    sub_ids = category.subcategories.values_list('id', flat=True)
    products = Product.objects.filter(
        (Q(category=category) | Q(category_id__in=sub_ids)),
        is_active=True,
        skus__quantity__gt=0,
        skus__shipping_status='available'
    ).select_related('category').prefetch_related(
        'skus', 
        'skus__offers'
    ).distinct().order_by('-id')
    
    parents = Category.objects.filter(parent__isnull=True)
    categories = parents if parents.count() > 1 else Category.objects.all()

    return render(request, 'products/product_list.html', {
        'current_category': category, 
        'products': products,
        'categories': categories
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
