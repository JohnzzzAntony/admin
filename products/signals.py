from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, Category

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

@receiver(post_save, sender=Product)
def product_saved(sender, instance, **kwargs):
    update_category_branch_counts(instance.category)

@receiver(post_delete, sender=Product)
def product_deleted(sender, instance, **kwargs):
    update_category_branch_counts(instance.category)
