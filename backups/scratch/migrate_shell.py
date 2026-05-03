from pages.models import Service
from products.models import Category, Product

# 1. Prosthetics & Orthotics Services
cat = Category.objects.filter(name__icontains='Prosthetics & Orthotics').first()
if cat:
    s, created = Service.objects.get_or_create(
        title='Prosthetics & Orthotics Services',
        defaults={
            'description': cat.description or 'Comprehensive prosthetic and orthotic care.',
            'order': 7,
            'icon_svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="m7 7 10 10"/><path d="m17 7-10 10"/></svg>'
        }
    )
    if created: print(f"Created Service: {s.title}")

# 2. Sensory Room Installations
prod = Product.objects.filter(name__icontains='Sensory Room Installations').first()
if prod:
    s, created = Service.objects.get_or_create(
        title='Sensory Room Installations',
        defaults={
            'description': prod.overview[:200] if prod.overview else 'Expert sensory environment setup.',
            'order': 8,
            'icon_svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z"/></svg>'
        }
    )
    if created: print(f"Created Service: {s.title}")
