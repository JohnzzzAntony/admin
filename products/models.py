from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from ckeditor.fields import RichTextField
from decimal import Decimal

# ─── Category ────────────────────────────────────────────────────────────────

class Category(models.Model):
    parent = models.ForeignKey(
        'self', 
        related_name='subcategories', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE,
        db_index=True,
        help_text="The immediate parent of this category. Leave blank for a top-level category."
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, help_text="Optional description for SEO and category page header.")
    image = models.ImageField(
        upload_to='categories/', 
        null=True, 
        blank=True, 
        help_text="Recommended: 512x512px. JPG, PNG, WEBP. Max 1MB."
    )
    image_url = models.URLField(blank=True, null=True, help_text="Alternative: Direct link to an externally hosted image.")
    icon_svg = models.TextField(blank=True, help_text="Paste SVG icon code here. Used if provided.")
    
    # Meta / Controls
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Status", choices=((True, 'Active'), (False, 'Remove')))
    show_on_homepage = models.BooleanField(default=False, verbose_name="Homepage Display", choices=((True, 'Enabled'), (False, 'Disabled')))
    homepage_order   = models.PositiveIntegerField(default=0, verbose_name="Homepage Display Order")

    # SEO Fields
    meta_title = models.CharField(max_length=255, blank=True, verbose_name="Meta Title")
    meta_description = models.TextField(blank=True, verbose_name="Meta Description")
    meta_keywords = models.TextField(blank=True, verbose_name="Meta Keywords")
    
    @property
    def get_image_url(self):
        try:
            if self.image: return self.image.url
            if self.image_url and "placeholder.com" not in self.image_url: return self.image_url
        except Exception: pass
        return "https://via.placeholder.com/300"

    def get_all_children(self, include_self=True):
        children = [self] if include_self else []
        for sub in self.subcategories.all():
            children.extend(sub.get_all_children(include_self=True))
        return children

    @property
    def active_subcategories(self):
        return self.subcategories.all()

    def get_ancestors(self):
        ancestors = []
        curr = self.parent
        while curr:
            ancestors.insert(0, curr)
            curr = curr.parent
        return ancestors

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.parent:
            curr = self.parent
            while curr:
                if curr == self:
                    raise ValidationError("Circular relationship detected: A category cannot be its own ancestor.")
                curr = curr.parent

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
        except Exception:
            pass # Validation will be handled by the form layer if possible
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    def get_absolute_url(self):
        from django.urls import reverse
        ancestors = self.get_ancestors()
        if ancestors:
            path = "/".join([a.slug for a in ancestors] + [self.slug])
            return reverse('products:category_hierarchy_detail', kwargs={'hierarchy_path': path})
        return reverse('products:category_detail', kwargs={'slug': self.slug})

    @property
    def total_product_count(self):
        """Recursive count of products in this category and all its children."""
        from .models import Product
        child_ids = [c.id for c in self.get_all_children(include_self=True)]
        return Product.objects.filter(category_id__in=child_ids, is_active=True).count()

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['homepage_order', 'name']

# ─── Product ─────────────────────────────────────────────────────────────────

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(
        upload_to='products/', 
        null=True, 
        blank=True,
        help_text="Primary Product Image."
    )
    image_url = models.URLField(blank=True, null=True, help_text="Alternative: Direct link to an externally hosted image.")

    # Inventory & Details
    sku_id = models.CharField(max_length=50, unique=True, blank=True, verbose_name="SKU ID")
    quantity = models.IntegerField(default=0, verbose_name="In-Stock Quantity")
    unit = models.CharField(max_length=20, choices=[('pcs', 'Pieces'), ('box', 'Box'), ('set', 'Set')], default='pcs')
    
    regular_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    shipping_status = models.CharField(max_length=50, choices=[
        ('available', 'In Stock'), ('out_of_stock', 'Out of Stock'), ('pre_order', 'Pre-Order')
    ], default='available')
    free_shipping = models.BooleanField(default=False, verbose_name="Free Shipping", choices=((True, 'Enabled'), (False, 'Disabled')))
    additional_shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_time = models.CharField(max_length=100, blank=True)

    # Dimensions
    weight = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    # Simplified Content
    features = models.TextField(help_text="Key features (one per line)", blank=True)
    overview = RichTextField(blank=True, null=True)
    technical_info = RichTextField(blank=True, null=True, verbose_name="Product Characteristics & Specifications")
    brochure = models.FileField(upload_to='brochures/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    show_on_homepage = models.BooleanField(default=False, verbose_name="Homepage Display", choices=((True, 'Enabled'), (False, 'Disabled')))
    is_active = models.BooleanField(default=True, verbose_name="Status", choices=((True, 'Active'), (False, 'Remove')))

    # SEO Fields (Multilingual)
    # SEO Fields
    meta_title = models.CharField(max_length=255, blank=True, verbose_name="Meta Title")
    meta_description = models.TextField(blank=True, verbose_name="Meta Description")
    meta_keywords = models.TextField(blank=True, verbose_name="Meta Keywords")
    
    @property
    def get_image_url(self):
        try:
            if self.image: return self.image.url
            if self.image_url: return self.image_url
        except Exception: pass
        return "https://via.placeholder.com/600x400"

    def get_best_price_info(self):
        from django.utils import timezone
        reg = self.regular_price or 0
        sale = self.sale_price or reg
        
        # Check for active offers if they exist
        now = timezone.now()
        active_offers = self.offers.filter(
            start_date__lte=now,
            end_date__gte=now
        )
        
        offer_price = sale
        for offer in active_offers:
            current_offer_price = reg
            if offer.offer_type == 'percentage':
                current_offer_price = reg * (1 - (offer.discount_value / 100))
            elif offer.offer_type == 'fixed':
                current_offer_price = reg - offer.discount_value
            elif offer.offer_type == 'final':
                current_offer_price = offer.discount_value
            
            if current_offer_price < offer_price:
                offer_price = current_offer_price
        
        final_price = offer_price
        discount_amount = reg - final_price
        discount_pct = 0
        if reg > 0:
            discount_pct = (discount_amount / reg) * 100
        
        ship = self.additional_shipping_charge or 0 if not self.free_shipping else 0
        
        return {
            'has_offer': final_price < reg,
            'final_price': round(final_price, 2),
            'regular_price': round(reg, 2),
            'discount_amount': round(discount_amount, 2),
            'discount_percentage': int(discount_pct),
            'discount_display': f"{int(discount_pct)}% OFF" if final_price < reg else None,
            'shipping_charge': ship,
            'free_shipping': self.free_shipping,
            'total_with_shipping': round(final_price + ship, 2)
        }

    @property
    def discount_percentage(self):
        info = self.get_best_price_info()
        return info.get('discount_percentage', 0)

    def is_in_stock(self): return self.quantity > 0 and self.shipping_status == 'available'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            if not self.slug: # Fallback for non-latin names
                self.slug = "product-" + timezone.now().strftime("%Y%m%d%H%M%S")
        
        if not self.sku_id:
            import random, string
            prefix = slugify(self.name)[:10].upper() or "PRO"
            self.sku_id = f"PRO-{prefix}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=4))}"
        super().save(*args, **kwargs)

    def __str__(self): return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/', null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['order']
    def get_image_url(self):
        if self.image: return self.image.url
        return self.image_url or "https://via.placeholder.com/300"

class Offer(models.Model):
    OFFER_TYPES = (
        ('percentage', 'Percentage Discount (%)'),
        ('fixed', 'Fixed Discount Entry (AED)'),
        ('final', 'Final Set Price (AED)'),
    )
    name = models.CharField(max_length=100)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product, related_name='offers', blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    def __str__(self): return self.name

class Collection(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    banner = models.ImageField(upload_to='collections/', null=True, blank=True)
    banner_url = models.URLField(blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='collections', blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, verbose_name="Status", choices=((True, 'Active'), (False, 'Remove')))
    
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self): return self.name
    class Meta: ordering = ['display_order']
