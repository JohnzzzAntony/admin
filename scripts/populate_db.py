import os
import django
from django.core.files.base import ContentFile
import urllib.request
import textwrap

import sys
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from products.models import Category, Product, ProductSKU, ProductImage
from pages.models import AboutUs, MissionVision, Service, Counter, WhyUsCard, GalleryItem, Partner
from core.models import SiteSettings, Testimonial, Client, SocialPost, StoreLocation
from sliders.models import HeroSlider

def populate():
    print("Clearing old data...")
    Category.objects.all().delete()
    AboutUs.objects.all().delete()
    MissionVision.objects.all().delete()
    Service.objects.all().delete()
    HeroSlider.objects.all().delete()
    SiteSettings.objects.all().delete()
    Partner.objects.all().delete()

    print("Creating Site Settings...")
    SiteSettings.objects.create(
        site_name="JKR International",
        header_title="JKR International",
        header_subtitle="JOY OF MOBILITY",
        email="info@jkrintl.com",
        phone="+971 4 251 5383",
        dubai_address="Office No. 2, Lootah Building, Marrakeh St, Umm Al Rammool, Rashidiya, Dubai",
        footer_copyright_text="© 2024 JKR International. All rights reserved.",
        fav_text="JKR"
    )

    print("Creating Categories...")
    cats = [
        "Compression Stockings", "Exercise Therapy", "Homecare", 
        "Hospital Equipment & Furniture", "Orthopedic Products", 
        "Physiotherapy & Rehabilitation", "Prosthetics & Orthotics",
        "Seating & Positioning System", "Walking & Standing Aids", "Wheelchairs"
    ]
    
    cat_objs = {}
    for c in cats:
        cat_objs[c] = Category.objects.create(
            name=c,
            meta_title=f"{c} - JKR International",
            meta_description=f"Best {c} in UAE with top quality."
        )

    print("Creating Products...")
    products_data = [
        ("medi Armschlinge", "Orthopedic Products", "Comfortable arm sling for injury recovery.", 45.00, "https://jkrintl.com/wp-content/uploads/2022/12/medi-Armschlinge.jpg"),
        ("duomed® smooth", "Compression Stockings", "Smooth and effective compression stockings for daily use.", 120.00, "https://jkrintl.com/wp-content/uploads/2022/12/duomed-smooth.jpg"),
        ("iCHAIR MC1 LIGHT 1.610", "Wheelchairs", "Advanced lightweight electric wheelchair.", 2500.00, "https://jkrintl.com/wp-content/uploads/2022/12/ichair-mc1.jpg"),
        ("Flash 1.135", "Wheelchairs", "Dynamic and rapid mobility wheelchair.", 1800.00, "https://jkrintl.com/wp-content/uploads/2022/12/Flash.jpg"),
    ]

    for title, cat, desc, price, img in products_data:
        p = Product.objects.create(
            category=cat_objs[cat],
            name=title,
            overview=desc,
            regular_price=price,
            image_url=img,
            is_active=True
        )
        ProductSKU.objects.create(
            product=p,
            sku_id=f"SKU-{title.split()[0].upper()}-001",
            quantity=15,
            unit="pcs",
            weight=1.5, length=10, width=10, height=10,
            additional_shipping_charge=5.00,
            delivery_time="2-3 Days",
            shipping_status="available"
        )
    
    print("Creating CMS/Homepage Blocks...")
    HeroSlider.objects.create(
        title="Redefining Mobility Excellence",
        subtitle="Top-tier medical solutions to Hospitals, Pharmacies, and Healthcare facilities",
        button_text="Shop Now",
        button_link="/products/",
        is_active=True
    )

    AboutUs.objects.create(
        title="About Us",
        heading="We craft solutions that enhance and Simplify Lives.",
        content="<p>JKR International is a trusted Medical Equipment Supplier in UAE, providing high-quality wheelchairs, rehabilitation products, and expert guidance. Joy, Knowledge, Responsibility are our core values.</p>",
    )

    MissionVision.objects.create(
        section_type='mission',
        title="Our Mission",
        content="To be the Company of Choice that provides quality medical devices, designed to enable, enhance and enrich the lives of our people."
    )

    Service.objects.create(title="High-Quality Products", description="Our innovative mobility products of the highest industry standards.")
    Service.objects.create(title="Customer Satisfaction", description="Attendant personally and professionally to deliver the best mobility solutions.")
    Service.objects.create(title="After Sales Support", description="A team of qualified engineers and technicians available on call.")

    Counter.objects.create(title="Partnerships", value="100+")
    Counter.objects.create(title="Products Delivered", value="1500+")

    WhyUsCard.objects.create(
        title="Expert Advice",
        description="We offer expert guidance to help our clients adapt to the rising costs of quality healthcare.",
        icon_svg='<svg fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a8 8 0 100 16 8 8 0 000-16zM9 9a1 1 0 012 0v4a1 1 0 11-2 0V9zm1-5a1.5 1.5 0 110 3 1.5 1.5 0 010-3z"></path></svg>'
    )

    Partner.objects.create(name="medi", website_url="https://www.medi.de/en/", logo_url="https://jkrintl.com/wp-content/uploads/2022/12/medi-logo.png")
    Partner.objects.create(name="Meyra", website_url="https://www.meyra.com/", logo_url="https://jkrintl.com/wp-content/uploads/2022/12/Meyra-logo.png")
    Partner.objects.create(name="Sissel", website_url="https://www.sissel.com/", logo_url="https://jkrintl.com/wp-content/uploads/2022/12/Sissel-logo.png")

    print("Creating Testimonials & Clients...")
    Testimonial.objects.create(client_name="Sarah Johnson", position="Health Specialist", content="JKR provided excellent support for our clinic's mobility needs. The equipment is top-notch.", rating=5)
    Client.objects.create(name="Dubai Health Authority", category='Public', logo_url="https://jkrintl.com/wp-content/uploads/2022/12/DHA-Logo.png")

    print("Success! Database populated with rich mock data.")

if __name__ == '__main__':
    populate()
