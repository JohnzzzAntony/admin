from django.core.management.base import BaseCommand
from products.models import Category, Product

class Command(BaseCommand):
    help = 'Recalculates and updates the denormalized product_count for all categories.'

    def handle(self, *args, **options):
        self.stdout.write('Starting category product count synchronization...')
        
        # We process leaf categories first, but actually since we use get_descendant_ids
        # which is independent of denormalized counts, we can just loop through all.
        categories = Category.objects.all()
        total = categories.count()
        
        for i, category in enumerate(categories):
            # Get all descendant IDs using the optimized method
            child_ids = category.get_descendant_ids(include_self=True)
            new_count = Product.objects.filter(category_id__in=child_ids, is_active=True).count()
            
            if category.product_count != new_count:
                category.product_count = new_count
                category.save(update_fields=['product_count'])
                self.stdout.write(self.style.SUCCESS(f'Updated "{category.name}": {new_count}'))
            else:
                self.stdout.write(f'Skipped "{category.name}": Already {new_count}')
            
            if (i + 1) % 10 == 0:
                self.stdout.write(f'Progress: {i + 1}/{total}')

        self.stdout.write(self.style.SUCCESS('Successfully synchronized all category product counts.'))
