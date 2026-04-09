"""
Comprehensive Demo Data Seeding Script for JKR E-commerce Platform
Run with: python manage.py shell < scripts/seed_demo_data.py
Or: python seed_all.py
"""
import os
import sys
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from decimal import Decimal

print("🚀 Starting Demo Data Seeding...")

# ── 1. Create superuser if not exists ──────────────────────────────────────────
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@demo.com', 'admin123')
    print("✅ Superuser created: admin / admin123")
else:
    print("ℹ️  Superuser already exists")

# ── 2. Site Settings ───────────────────────────────────────────────────────────
from core.models import SiteSettings, Testimonial, Client, SocialPost
from core.design_models import DesignSettings

ss, _ = SiteSettings.objects.get_or_create(id=1)
ss.site_name = "MediSupply Pro"
ss.company_name = "MediSupply International FZ LLC"
ss.logo_url = "https://via.placeholder.com/400x100/114084/ffffff?text=MediSupply+Pro"
ss.email = "info@medisupply.ae"
ss.phone = "+971 4 123 4567"
ss.whatsapp = "+971 50 123 4567"
ss.branch1_name = "Dubai"
ss.dubai_address = "Business Bay, Sheikh Zayed Road, Dubai, UAE"
ss.branch2_name = "Abu Dhabi"
ss.abudhabi_address = "Khalidiyah Street, Abu Dhabi, UAE"
ss.facebook = "https://facebook.com"
ss.instagram = "https://instagram.com"
ss.linkedin = "https://linkedin.com"
ss.meta_title = "MediSupply Pro - Premium Medical Equipment Supplier in UAE"
ss.meta_description = "Leading supplier of medical equipment and healthcare supplies across UAE. Quality products, trusted service."
ss.save()
print("✅ Site Settings configured")

ds, _ = DesignSettings.objects.get_or_create(id=1)
ds.primary_color = "#114084"
ds.secondary_color = "#005CB9"
ds.hp_collections_title = 'Exclusive <span class="text-primary">Collections</span>'
ds.hp_collections_subtitle = "Handpicked selection of premium medical equipment and essential supplies."
ds.hp_partners_title = "We Deal with,"
ds.hp_partners_subtitle = "100+ trusted manufacturing partnerships ensuring the quality of every product we distribute."
ds.hp_services_title = "Specialized Medical Services"
ds.hp_services_subtitle = "We are dedicated to maintaining the health and effectiveness of your essential diagnostic equipment."
ds.save()
print("✅ Design Settings configured")

# ── 3. Hero Sliders ────────────────────────────────────────────────────────────
from sliders.models import HeroSlider

sliders_data = [
    {
        "title": "Premium Medical Equipment",
        "subtitle": "TRUSTED BY 500+ HOSPITALS",
        "image_url": "https://images.unsplash.com/photo-1584982751601-97dcc096659c?w=1920&q=80",
        "button_text": "Explore Products",
        "button_link": "/products/",
        "order": 1,
    },
    {
        "title": "Advanced Diagnostic Solutions",
        "subtitle": "ISO CERTIFIED SUPPLIER",
        "image_url": "https://images.unsplash.com/photo-1631815588090-d4bfec5b1ccb?w=1920&q=80",
        "button_text": "Get a Quote",
        "button_link": "/contact-us/",
        "order": 2,
    },
    {
        "title": "Surgical & ICU Equipment",
        "subtitle": "24/7 TECHNICAL SUPPORT",
        "image_url": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=1920&q=80",
        "button_text": "Browse Catalogue",
        "button_link": "/products/",
        "order": 3,
    },
]

HeroSlider.objects.all().delete()
for s in sliders_data:
    HeroSlider.objects.create(**s)
print(f"✅ {len(sliders_data)} Hero Sliders created")

# ── 4. Categories ──────────────────────────────────────────────────────────────
from products.models import Category, Product, Collection, Offer

categories_data = [
    {"name": "Diagnostic Equipment", "image_url": "https://images.unsplash.com/photo-1584982751601-97dcc096659c?w=300&q=80", "show_on_homepage": True, "homepage_order": 1},
    {"name": "Surgical Instruments", "image_url": "https://images.unsplash.com/photo-1551601651-2a8555f1a136?w=300&q=80", "show_on_homepage": True, "homepage_order": 2},
    {"name": "Patient Monitoring", "image_url": "https://images.unsplash.com/photo-1530026186672-2cd00ffc50fe?w=300&q=80", "show_on_homepage": True, "homepage_order": 3},
    {"name": "ICU & Critical Care", "image_url": "https://images.unsplash.com/photo-1631815588090-d4bfec5b1ccb?w=300&q=80", "show_on_homepage": True, "homepage_order": 4},
    {"name": "Rehabilitation", "image_url": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=300&q=80", "show_on_homepage": True, "homepage_order": 5},
    {"name": "Laboratory Supplies", "image_url": "https://images.unsplash.com/photo-1576086213369-97a306d36557?w=300&q=80", "show_on_homepage": True, "homepage_order": 6},
]

Category.objects.all().delete()
cats = {}
for c in categories_data:
    from django.utils.text import slugify
    slug = slugify(c['name'])
    cat = Category(
        name=c['name'],
        slug=slug,
        image_url=c['image_url'],
        show_on_homepage=c['show_on_homepage'],
        homepage_order=c['homepage_order'],
        description=f"High-quality {c['name'].lower()} sourced from certified international manufacturers."
    )
    cat.save()
    cats[c['name']] = cat
print(f"✅ {len(cats)} Categories created")

# ── 5. Products ────────────────────────────────────────────────────────────────
products_data = [
    # Diagnostic Equipment
    {"name": "Digital X-Ray System", "category": "Diagnostic Equipment", "regular_price": 45000, "sale_price": 38500, "quantity": 5, "image_url": "https://images.unsplash.com/photo-1626417565769-ea0f5e81e72c?w=600&q=80"},
    {"name": "Portable Ultrasound Machine", "category": "Diagnostic Equipment", "regular_price": 28000, "sale_price": 24500, "quantity": 8, "image_url": "https://images.unsplash.com/photo-1530026186672-2cd00ffc50fe?w=600&q=80"},
    {"name": "ECG / 12-Lead Machine", "category": "Diagnostic Equipment", "regular_price": 8500, "sale_price": None, "quantity": 15, "image_url": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=600&q=80"},
    {"name": "Blood Glucose Monitor", "category": "Diagnostic Equipment", "regular_price": 450, "sale_price": 380, "quantity": 50, "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=600&q=80"},
    # Surgical Instruments
    {"name": "Laparoscopic Surgery Set", "category": "Surgical Instruments", "regular_price": 18000, "sale_price": None, "quantity": 3, "image_url": "https://images.unsplash.com/photo-1551601651-2a8555f1a136?w=600&q=80"},
    {"name": "Surgical Forceps Set (10 Piece)", "category": "Surgical Instruments", "regular_price": 2800, "sale_price": 2400, "quantity": 20, "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&q=80"},
    {"name": "Disposable Scalpel Blades (Box)", "category": "Surgical Instruments", "regular_price": 350, "sale_price": None, "quantity": 100, "image_url": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=600&q=80"},
    {"name": "Retractor Set - Abdominal", "category": "Surgical Instruments", "regular_price": 4200, "sale_price": 3800, "quantity": 7, "image_url": "https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=600&q=80"},
    # Patient Monitoring
    {"name": "Multi-Parameter Patient Monitor", "category": "Patient Monitoring", "regular_price": 12500, "sale_price": 10900, "quantity": 10, "image_url": "https://images.unsplash.com/photo-1631815588090-d4bfec5b1ccb?w=600&q=80"},
    {"name": "Pulse Oximeter - Fingertip", "category": "Patient Monitoring", "regular_price": 280, "sale_price": 220, "quantity": 200, "image_url": "https://images.unsplash.com/photo-1584982751601-97dcc096659c?w=600&q=80"},
    {"name": "Digital Blood Pressure Monitor", "category": "Patient Monitoring", "regular_price": 650, "sale_price": None, "quantity": 80, "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=600&q=80"},
    {"name": "Bedside Cardiac Monitor", "category": "Patient Monitoring", "regular_price": 22000, "sale_price": 19500, "quantity": 4, "image_url": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=600&q=80"},
    # ICU & Critical Care
    {"name": "ICU Ventilator - Advanced", "category": "ICU & Critical Care", "regular_price": 95000, "sale_price": None, "quantity": 2, "image_url": "https://images.unsplash.com/photo-1530026186672-2cd00ffc50fe?w=600&q=80"},
    {"name": "Syringe Infusion Pump", "category": "ICU & Critical Care", "regular_price": 5500, "sale_price": 4800, "quantity": 12, "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&q=80"},
    {"name": "Hospital Bed - Electric", "category": "ICU & Critical Care", "regular_price": 8800, "sale_price": 7500, "quantity": 6, "image_url": "https://images.unsplash.com/photo-1631815588090-d4bfec5b1ccb?w=600&q=80"},
    # Rehabilitation
    {"name": "Physiotherapy Ultrasound Unit", "category": "Rehabilitation", "regular_price": 4500, "sale_price": None, "quantity": 9, "image_url": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=600&q=80"},
    {"name": "TENS/EMS Therapy Device", "category": "Rehabilitation", "regular_price": 1200, "sale_price": 980, "quantity": 25, "image_url": "https://images.unsplash.com/photo-1584982751601-97dcc096659c?w=600&q=80"},
    {"name": "Traction Therapy Table", "category": "Rehabilitation", "regular_price": 15000, "sale_price": None, "quantity": 3, "image_url": "https://images.unsplash.com/photo-1576086213369-97a306d36557?w=600&q=80"},
    # Lab Supplies
    {"name": "Laboratory Centrifuge", "category": "Laboratory Supplies", "regular_price": 9800, "sale_price": 8200, "quantity": 5, "image_url": "https://images.unsplash.com/photo-1576086213369-97a306d36557?w=600&q=80"},
    {"name": "Digital Microscope - LED", "category": "Laboratory Supplies", "regular_price": 7500, "sale_price": None, "quantity": 7, "image_url": "https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=600&q=80"},
    {"name": "Autoclave Sterilizer 24L", "category": "Laboratory Supplies", "regular_price": 6200, "sale_price": 5400, "quantity": 4, "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&q=80"},
]

Product.objects.all().delete()
products = {}
for i, p in enumerate(products_data):
    from django.utils.text import slugify
    name = p['name']
    slug = slugify(name)
    cat = cats[p['category']]
    sale = Decimal(str(p['sale_price'])) if p['sale_price'] else None
    prod = Product(
        name=name,
        slug=slug,
        sku_id=f"SKU-{1000+i:04d}",
        category=cat,
        regular_price=Decimal(str(p['regular_price'])),
        sale_price=sale,
        quantity=p['quantity'],
        shipping_status='available',
        image_url=p['image_url'],
        overview=f"<p>High-quality {name} sourced from certified international manufacturers. Suitable for clinical and hospital use. Comes with full warranty and technical support.</p>",
        features=f"<ul><li>ISO Certified</li><li>2 Year Warranty</li><li>Technical Support Included</li><li>FDA Approved</li></ul>",
        show_on_homepage=True,
        weight=5.0,
        unit="pcs",
    )
    prod.save()
    products[name] = prod

print(f"✅ {len(products)} Products created")

# ── 6. Collections ─────────────────────────────────────────────────────────────
Collection.objects.all().delete()
all_prods = list(Product.objects.all())
collections_data = [
    {"name": "Hospital Essentials", "slug": "hospital-essentials", "display_order": 1, "products": all_prods[:7], "banner_url": "https://images.unsplash.com/photo-1631815588090-d4bfec5b1ccb?w=1200&q=80"},
    {"name": "Diagnostic Suite", "slug": "diagnostic-suite", "display_order": 2, "products": all_prods[7:14], "banner_url": "https://images.unsplash.com/photo-1584982751601-97dcc096659c?w=1200&q=80"},
    {"name": "Surgical Bundle", "slug": "surgical-bundle", "display_order": 3, "products": all_prods[14:], "banner_url": "https://images.unsplash.com/photo-1551601651-2a8555f1a136?w=1200&q=80"},
]

for c in collections_data:
    col = Collection(name=c['name'], slug=c['slug'], display_order=c['display_order'], banner_url=c.get('banner_url',''))
    col.save()
    col.products.set(c['products'])
print(f"✅ {len(collections_data)} Collections created")

# ── 7. Pages Content (About, Services, etc.) ───────────────────────────────────
from pages.models import AboutUs, Service, Counter, WhyUsCard, Partner, GalleryItem, MissionVision

AboutUs.objects.all().delete()
about = AboutUs(
    heading="Your Trusted Medical Equipment Partner Since 2005",
    content="<p>MediSupply Pro is a leading supplier of premium medical equipment and healthcare solutions in the UAE. With over 18 years of experience, we partner with the world's top manufacturers to deliver ISO-certified equipment to hospitals, clinics, and healthcare facilities across the Middle East.</p><p>Our team of certified biomedical engineers provides complete lifecycle support — from procurement and installation to maintenance and training.</p>",
)
about.save()
print("✅ About Us created")

Service.objects.all().delete()
services_data = [
    {"title": "Equipment Installation", "description": "Professional installation and commissioning of all medical equipment by certified biomedical engineers.", "order": 1, "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" viewBox="0 0 16 16"><path d="M9.405 1.05c-.413-1.4-2.397-1.4-2.81 0l-.1.34a1.464 1.464 0 0 1-2.105.872l-.31-.17c-1.283-.698-2.686.705-1.987 1.987l.169.311c.446.82.023 1.841-.872 2.105l-.34.1c-1.4.413-1.4 2.397 0 2.81l.34.1a1.464 1.464 0 0 1 .872 2.105l-.17.31c-.698 1.283.705 2.686 1.987 1.987l.311-.169a1.464 1.464 0 0 1 2.105.872l.1.34c.413 1.4 2.397 1.4 2.81 0l.1-.34a1.464 1.464 0 0 1 2.105-.872l.31.17c1.283.698 2.686-.705 1.987-1.987l-.169-.311a1.464 1.464 0 0 1 .872-2.105l.34-.1c1.4-.413 1.4-2.397 0-2.81l-.34-.1a1.464 1.464 0 0 1-.872-2.105l.17-.31c.698-1.283-.705-2.686-1.987-1.987l-.311.169a1.464 1.464 0 0 1-2.105-.872l-.1-.34zM8 10.93a2.929 2.929 0 1 1 0-5.86 2.929 2.929 0 0 1 0 5.858z"/></svg>'},
    {"title": "Preventive Maintenance", "description": "Scheduled maintenance programs to keep your equipment in peak operating condition and extend service life.", "order": 2, "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z"/></svg>'},
    {"title": "Emergency Repair", "description": "24/7 emergency repair services to minimize downtime and keep your facility running smoothly.", "order": 3, "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" viewBox="0 0 16 16"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>'},
    {"title": "Staff Training", "description": "Comprehensive operator training programs for medical and technical staff on equipment usage and safety protocols.", "order": 4, "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" viewBox="0 0 16 16"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/><path fill-rule="evenodd" d="M5.216 14A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216z"/><path d="M4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>'},
    {"title": "Spare Parts Supply", "description": "Genuine OEM spare parts and accessories available for all major medical equipment brands we supply.", "order": 5, "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" viewBox="0 0 16 16"><path d="M11 2a3 3 0 0 1 3 3v6a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3V5a3 3 0 0 1 3-3h6zM5 1a4 4 0 0 0-4 4v6a4 4 0 0 0 4 4h6a4 4 0 0 0 4-4V5a4 4 0 0 0-4-4H5z"/><path d="M8 7.993c1.664-1.711 5.825 1.283 0 5.132-5.825-3.85-1.664-6.843 0-5.132z"/></svg>'},
    {"title": "Calibration Services", "description": "Precision calibration and performance verification services compliant with ISO 17025 standards.", "order": 6, "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" viewBox="0 0 16 16"><path d="M4 .5a.5.5 0 0 0-1 0V1H2a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2h-1V.5a.5.5 0 0 0-1 0V1H4V.5zM1 4h14v10a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V4z"/></svg>'},
]
for s in services_data:
    Service.objects.create(**s)
print(f"✅ {len(services_data)} Services created")

Counter.objects.all().delete()
counters_data = [
    {"title": "Happy Clients", "value": "500+", "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" viewBox="0 0 16 16"><path d="M3 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H3zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/></svg>', "order": 1},
    {"title": "Products Supplied", "value": "800+", "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" viewBox="0 0 16 16"><path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H14.5a.5.5 0 0 1 .491.592l-1.5 8A.5.5 0 0 1 13 12H4a.5.5 0 0 1-.491-.408L2.01 3.607 1.61 2H.5a.5.5 0 0 1-.5-.5z"/></svg>', "order": 2},
    {"title": "Years Experience", "value": "18+", "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="M7.5 4a.5.5 0 0 0-1 0v3.5H4a.5.5 0 0 0 0 1h3a.5.5 0 0 0 .5-.5V4z"/></svg>', "order": 3},
    {"title": "Countries Served", "value": "12", "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" viewBox="0 0 16 16"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm7.5-6.923c-.67.204-1.335.82-1.887 1.855A7.97 7.97 0 0 0 5.145 4H7.5V1.077zM4.09 4a9.267 9.267 0 0 1 .64-1.539 6.7 6.7 0 0 1 .597-.933A7.025 7.025 0 0 0 2.255 4H4.09zm-.582 3.5c.033-.5.096-.988.198-1.46H1.05A7.032 7.032 0 0 0 1 7.5h2.508zM7.5 15.93V13H5.145a9.133 9.133 0 0 0 1.013 1.486 11.06 11.06 0 0 0 .44.444 7.167 7.167 0 0 0 .902 1zm-2.372-2.43H7.5V7.5H4.862a23.336 23.336 0 0 0-.23 3.5 23.333 23.333 0 0 0 .23 3.5z"/></svg>', "order": 4},
]
for c in counters_data:
    Counter.objects.create(**c)
print(f"✅ {len(counters_data)} Counters created")

WhyUsCard.objects.all().delete()
why_us_data = [
    {"title": "ISO 9001 Certified", "description": "All our products meet international quality standards with complete documentation and certification.", "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M2.5 8a5.5 5.5 0 0 1 8.25-4.764.5.5 0 0 0 .5-.866A6.5 6.5 0 1 0 14.5 8a.5.5 0 0 0-1 0 5.5 5.5 0 1 1-11 0z"/><path d="M15.354 3.354a.5.5 0 0 0-.708-.708L8 9.293 5.354 6.646a.5.5 0 1 0-.708.708l3 3a.5.5 0 0 0 .708 0l7-7z"/></svg>', "order": 1},
    {"title": "Fast Delivery", "description": "Efficient logistics network ensures prompt delivery across the UAE and neighboring countries.", "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M0 3.5A1.5 1.5 0 0 1 1.5 2h9A1.5 1.5 0 0 1 12 3.5V5h1.02a1.5 1.5 0 0 1 1.17.563l1.481 1.85a1.5 1.5 0 0 1 .329.938V10.5a1.5 1.5 0 0 1-1.5 1.5H14a2 2 0 1 1-4 0H5a2 2 0 1 1-3.998-.085A1.5 1.5 0 0 1 0 10.5v-7z"/></svg>', "order": 2},
    {"title": "24/7 Technical Support", "description": "Our certified biomedical engineers are available around the clock for any technical assistance.", "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M8 1a5 5 0 0 0-5 5v1h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a6 6 0 1 1 12 0v6a2.5 2.5 0 0 1-2.5 2.5H9.366a1 1 0 0 1-.866.5h-1a1 1 0 1 1 0-2h1a1 1 0 0 1 .866.5H11.5A1.5 1.5 0 0 0 13 12h-1a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1h1V6a5 5 0 0 0-5-5z"/></svg>', "order": 3},
    {"title": "Competitive Pricing", "description": "Direct manufacturer partnerships allow us to offer the best market prices without compromising quality.", "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M5.5 9.511c.076.954.83 1.697 2.182 1.785V12h.5v-.709c1.4-.098 2.218-.846 2.218-1.932 0-.987-.626-1.496-1.745-1.76l-.473-.112V5.57c.6.068.982.396 1.074.85h1.052c-.076-.919-.864-1.638-2.126-1.716V4h-.5v.54c-1.248.137-2.026.advised.868-1.858 0-.99.676-1.558 1.858-1.558 1.21 0 1.842.673 1.87 1.606h1.02v-.011c0 1.044-.755 1.686-2.044 1.82v-1.78c.502-.186.801-.5.8-.924 0-.45-.32-.748-.88-.748-.57 0-.9.26-.9.748z"/></svg>', "order": 4},
    {"title": "Genuine Products", "description": "All products are 100% genuine, sourced directly from authorized manufacturers with full warranties.", "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M5.338 1.59a61.44 61.44 0 0 0-2.837.856.481.481 0 0 0-.328.39c-.554 4.157.726 7.19 2.253 9.188a10.725 10.725 0 0 0 2.287 2.233c.346.244.652.42.893.533.12.057.218.095.293.118a.55.55 0 0 0 .101.025.615.615 0 0 0 .1-.025c.076-.023.174-.061.294-.118.24-.113.547-.29.893-.533a10.726 10.726 0 0 0 2.287-2.233c1.527-1.997 2.807-5.031 2.253-9.188a.48.48 0 0 0-.328-.39c-.651-.213-1.75-.56-2.837-.855C9.552 1.29 8.531 1.067 8 1.067c-.53 0-1.552.223-2.662.524zM5.072.56C6.157.265 7.31 0 8 0s1.843.265 2.928.56c1.11.3 2.229.655 2.887.87a1.54 1.54 0 0 1 1.044 1.262c.596 4.477-.787 7.795-2.465 9.99a11.775 11.775 0 0 1-2.517 2.453 7.159 7.159 0 0 1-1.048.625c-.28.132-.581.24-.829.24s-.548-.108-.829-.24a7.158 7.158 0 0 1-1.048-.625 11.777 11.777 0 0 1-2.517-2.453C1.928 10.487.545 7.169 1.141 2.692A1.54 1.54 0 0 1 2.185 1.43 62.456 62.456 0 0 1 5.072.56z"/></svg>', "order": 5},
    {"title": "Easy Financing", "description": "Flexible payment and financing options available for large orders and institutional clients.", "icon_svg": '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4zm2-1a1 1 0 0 0-1 1v1h14V4a1 1 0 0 0-1-1H2zm13 4H1v5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V7z"/></svg>', "order": 6},
]
for w in why_us_data:
    WhyUsCard.objects.create(**w)
print(f"✅ {len(why_us_data)} Why Us cards created")

# Gallery
GalleryItem.objects.all().delete()
gallery_data = [
    {"title": "Hospital Installation", "image_url": "https://images.unsplash.com/photo-1631815588090-d4bfec5b1ccb?w=600&q=80", "order": 1},
    {"title": "Diagnostic Lab", "image_url": "https://images.unsplash.com/photo-1576086213369-97a306d36557?w=600&q=80", "order": 2},
    {"title": "Medical Team Training", "image_url": "https://images.unsplash.com/photo-1584982751601-97dcc096659c?w=600&q=80", "order": 3},
    {"title": "Equipment Showcase", "image_url": "https://images.unsplash.com/photo-1551601651-2a8555f1a136?w=600&q=80", "order": 4},
    {"title": "ICU Setup", "image_url": "https://images.unsplash.com/photo-1530026186672-2cd00ffc50fe?w=600&q=80", "order": 5},
    {"title": "Surgical Theatre", "image_url": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=600&q=80", "order": 6},
    {"title": "Patient Recovery", "image_url": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=600&q=80", "order": 7},
    {"title": "Lab Operations", "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&q=80", "order": 8},
]
for g in gallery_data:
    GalleryItem.objects.create(**g)
print(f"✅ {len(gallery_data)} Gallery items created")

# Mission & Vision
MissionVision.objects.all().delete()
MissionVision.objects.create(
    section_type='mission',
    title='Our Mission',
    content='To provide healthcare institutions across the Middle East with cutting-edge medical equipment and unmatched technical support, ensuring better patient outcomes and operational excellence.',
    image_url='https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800&q=80',
)
MissionVision.objects.create(
    section_type='vision',
    title='Our Vision',
    content='To be the most trusted medical equipment partner in the GCC, recognized for quality, innovation, and a unwavering commitment to enhancing healthcare delivery.',
    image_url='https://images.unsplash.com/photo-1584982751601-97dcc096659c?w=800&q=80',
)
print("✅ Mission & Vision created")

# Partners
Partner.objects.all().delete()
partners_data = [
    {"name": "Philips Healthcare", "logo_url": "https://via.placeholder.com/200x80/114084/ffffff?text=Philips", "order": 1},
    {"name": "Siemens Healthineers", "logo_url": "https://via.placeholder.com/200x80/005CB9/ffffff?text=Siemens", "order": 2},
    {"name": "GE Healthcare", "logo_url": "https://via.placeholder.com/200x80/114084/ffffff?text=GE+Health", "order": 3},
    {"name": "Mindray", "logo_url": "https://via.placeholder.com/200x80/005CB9/ffffff?text=Mindray", "order": 4},
    {"name": "Draeger", "logo_url": "https://via.placeholder.com/200x80/114084/ffffff?text=Draeger", "order": 5},
    {"name": "Medtronic", "logo_url": "https://via.placeholder.com/200x80/005CB9/ffffff?text=Medtronic", "order": 6},
]
for p in partners_data:
    Partner.objects.create(**p)
print(f"✅ {len(partners_data)} Partners created")

# Testimonials
Testimonial.objects.all().delete()
testimonials_data = [
    {"client_name": "Dr. Ahmed Al-Rashidi", "position": "Chief Medical Officer, Dubai Hospital", "content": "MediSupply Pro has been our trusted partner for over 5 years. Their equipment quality and after-sales support are exceptional. Highly recommended for any healthcare institution.", "rating": 5, "image_url": "https://randomuser.me/api/portraits/men/32.jpg", "order": 1},
    {"client_name": "Dr. Sarah Johnson", "position": "Head of Radiology, Abu Dhabi Clinic", "content": "The digital X-ray system we purchased exceeded our expectations. Installation was professional and the training provided was comprehensive. Excellent service!", "rating": 5, "image_url": "https://randomuser.me/api/portraits/women/44.jpg", "order": 2},
    {"client_name": "Mr. Khalid Hassan", "position": "Hospital Administrator, Sharjah Medical Center", "content": "Prompt delivery, competitive pricing, and genuine products. MediSupply Pro makes procurement of medical equipment straightforward and reliable.", "rating": 5, "image_url": "https://randomuser.me/api/portraits/men/55.jpg", "order": 3},
]
for t in testimonials_data:
    Testimonial.objects.create(**t)
print(f"✅ {len(testimonials_data)} Testimonials created")

# Clients
Client.objects.all().delete()
clients_data = [
    {"name": "Dubai Health Authority", "logo_url": "https://via.placeholder.com/150x60/114084/ffffff?text=DHA", "category": "Public", "order": 1},
    {"name": "SEHA Abu Dhabi", "logo_url": "https://via.placeholder.com/150x60/005CB9/ffffff?text=SEHA", "category": "Public", "order": 2},
    {"name": "Ministry of Health UAE", "logo_url": "https://via.placeholder.com/150x60/114084/ffffff?text=MoH+UAE", "category": "Public", "order": 3},
    {"name": "Sharjah Health Authority", "logo_url": "https://via.placeholder.com/150x60/005CB9/ffffff?text=SHA", "category": "Public", "order": 4},
    {"name": "NMC Healthcare", "logo_url": "https://via.placeholder.com/150x60/114084/ffffff?text=NMC", "category": "Private", "order": 1},
    {"name": "Aster DM Healthcare", "logo_url": "https://via.placeholder.com/150x60/005CB9/ffffff?text=Aster", "category": "Private", "order": 2},
    {"name": "Burjeel Medical City", "logo_url": "https://via.placeholder.com/150x60/114084/ffffff?text=Burjeel", "category": "Private", "order": 3},
    {"name": "Mediclinic UAE", "logo_url": "https://via.placeholder.com/150x60/005CB9/ffffff?text=Mediclinic", "category": "Private", "order": 4},
]
for c in clients_data:
    Client.objects.create(**c)
print(f"✅ {len(clients_data)} Clients created")

# Social Posts
SocialPost.objects.all().delete()
social_data = [
    {"image_url": "https://images.unsplash.com/photo-1631815588090-d4bfec5b1ccb?w=400&q=80", "link": "https://instagram.com", "order": 1},
    {"image_url": "https://images.unsplash.com/photo-1584982751601-97dcc096659c?w=400&q=80", "link": "https://instagram.com", "order": 2},
    {"image_url": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400&q=80", "link": "https://instagram.com", "order": 3},
    {"image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&q=80", "link": "https://instagram.com", "order": 4},
    {"image_url": "https://images.unsplash.com/photo-1551601651-2a8555f1a136?w=400&q=80", "link": "https://instagram.com", "order": 5},
    {"image_url": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400&q=80", "link": "https://instagram.com", "order": 6},
]
for s in social_data:
    SocialPost.objects.create(**s)
print(f"✅ {len(social_data)} Social posts created")

# Promo Banners
from sliders.models import PromoBanner, BannerItem
PromoBanner.objects.all().delete()

banner1 = PromoBanner.objects.create(name="Mid-Year Sale Banner", layout="2_col", shape="rounded", homepage_order=3, is_active=True)
BannerItem.objects.create(banner_section=banner1, image_url="https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800&q=80", link="/products/", title="Up to 25% Off Surgical Sets", subtitle="Limited Time Offer", order=1)
BannerItem.objects.create(banner_section=banner1, image_url="https://images.unsplash.com/photo-1630959305168-da9f8e87e8b5?w=800&q=80", link="/products/", title="New Diagnostic Arrivals", subtitle="Shop Now", order=2)

print("✅ Promo Banners created")

print("\n" + "="*50)
print("🎉 ALL DEMO DATA SEEDED SUCCESSFULLY!")
print("="*50)
print("Admin URL:    http://localhost:8000/admin/")
print("Username:     admin")
print("Password:     admin123")
print("Frontend URL: http://localhost:8000/")
print("="*50)
