from products.models import Category
empty_slugs = Category.objects.filter(slug='')
print(f'Empty slugs: {empty_slugs.count()}')
for c in empty_slugs:
    print(c.name)
