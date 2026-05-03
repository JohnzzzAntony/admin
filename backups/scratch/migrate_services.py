from pages.models import Service
from products.models import Product, Category

def migrate():
    # 1. Sensory Room Installations
    sensory_product = Product.objects.filter(name__icontains='Sensory Room Installations').first()
    if sensory_product:
        service, created = Service.objects.get_or_create(
            title='Sensory Room Installations',
            defaults={
                'description': sensory_product.overview or 'Expert sensory room design and installation services.',
                'order': 8,
                'is_active': True,
                'icon_svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>'
            }
        )
        if created:
            print(f"Created Service: {service.title}")
        else:
            print(f"Service already exists: {service.title}")

    # 2. Prosthetics & Orthotics
    # (Already exists as ID 1, but let's ensure it has a good SVG and description if missing)
    po_service = Service.objects.filter(title__icontains='Prosthetics').first()
    if po_service:
        if not po_service.icon_svg:
            po_service.icon_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="m7 7 10 10"/><path d="m17 7-10 10"/></svg>'
            po_service.save()
            print(f"Updated SVG for {po_service.title}")

migrate()
