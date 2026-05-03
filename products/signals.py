from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product, Category, Brand


def update_category_branch_counts(category):
    """Updates counts for a category and all its ancestors efficiently."""
    if not category:
        return
        
    # Get all descendant IDs using the optimized method
    child_ids = category.get_descendant_ids(include_self=True)
    new_count = Product.objects.filter(category_id__in=child_ids, is_active=True).count()
    
    if category.product_count != new_count:
        category.product_count = new_count
        category.save(update_fields=['product_count'])
    
    # Update parents recursively (usually only 2-3 levels)
    if category.parent:
        update_category_branch_counts(category.parent)


def _bust_nav_cache():
    """Invalidate navigation context processor caches."""
    cache.delete('global_nav_categories_v1')


@receiver(post_save, sender=Product)
def product_saved(sender, instance, **kwargs):
    update_category_branch_counts(instance.category)


@receiver(post_delete, sender=Product)
def product_deleted(sender, instance, **kwargs):
    update_category_branch_counts(instance.category)


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def category_changed(sender, instance, **kwargs):
    """Bust the mega-menu cache whenever a category is changed."""
    _bust_nav_cache()


@receiver(post_save, sender=Brand)
@receiver(post_delete, sender=Brand)
def brand_changed(sender, instance, **kwargs):
    """Bust the mega-menu cache whenever a brand is changed."""
    _bust_nav_cache()

