import os
import django
import sys
import requests
import environ
from django.core.files.base import ContentFile
from io import BytesIO

sys.path.append('.')
env = environ.Env()
environ.Env.read_env()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from products.models import Category, Product, ProductSKU
from pages.models import AboutUs, MissionVision, Service, Counter, WhyUsCard, GalleryItem, Partner
from core.models import SiteSettings, Testimonial, Client, SocialPost, StoreLocation
from sliders.models import HeroSlider
import cloudinary.uploader

def upload_to_cloudinary(url):
    print(f"Uploading {url} to Cloudinary...")
    try:
        res = cloudinary.uploader.upload(url, timeout=20)
        return res.get('secure_url')
    except Exception as e:
        print(f"!!! Cloudinary upload failed for {url}: {e}")
        return None

def populate():
    print("Clearing old data...")
    Product.objects.all().delete()
    Category.objects.all().delete()
    HeroSlider.objects.all().delete()
    SiteSettings.objects.all().delete()
    Partner.objects.all().delete()

    print("Creating Site Settings...")
    logo_url = upload_to_cloudinary("https://jkrintl.com/wp-content/uploads/2022/02/cropped-jkr-logo-ful.png")
    SiteSettings.objects.create(
        site_name="JKR International",
        header_title="JKR International",
        header_subtitle="JOY OF MOBILITY",
        logo_url=logo_url,
        email="info@jkrintl.com",
        phone="+971 4 251 5383",
        dubai_address="Office No. 2, Lootah Building, Marrakeh St, Umm Al Rammool, Rashidiya, Dubai",
        footer_copyright_text="© 2024 JKR International. All rights reserved.",
        fav_text="JKR"
    )

    print("Creating Categories...")
    cats = [
        ("Wheelchairs", "https://jkrintl.com/wp-content/uploads/2025/12/csm_flash-meyra_a2f264dc9c.png"),
        ("Compression", "https://jkrintl.com/wp-content/uploads/2026/03/duomed-smooth-at-caramel-m-371343-150x150.webp")
    ]
    
    cat_objs = {}
    for name, url in cats:
        remote_url = upload_to_cloudinary(url)
        cat_objs[name] = Category.objects.create(name=name, image_url=remote_url, show_on_homepage=True)

    print("Creating Products...")
    products_data = [
        ("iCHAIR MC1 LIGHT", "Wheelchairs", "Advanced lightweight electric wheelchair.", 2500.00, "https://jkrintl.com/wp-content/uploads/2025/12/csm_Meyra_iCHAIR-MC1-Light_KVP_Stoerer_EN_0dfd07456e.png"),
        ("Flash 1.135", "Wheelchairs", "Dynamic and rapid mobility wheelchair.", 1800.00, "https://jkrintl.com/wp-content/uploads/2025/12/csm_flash-meyra_a2f264dc9c.png"),
        ("medi Armschlinge", "Wheelchairs", "Comfortable arm sling for injury recovery.", 45.00, "https://jkrintl.com/wp-content/uploads/2026/03/schlinge-schultergelenk-stabil-medi-armschlinge-m-20905-150x150.webp"),
    ]

    for title, cat, desc, price, url in products_data:
        remote_url = upload_to_cloudinary(url)
        p = Product.objects.create(
            category=cat_objs[cat],
            name=title,
            overview=desc,
            regular_price=price,
            image_url=remote_url,
            is_active=True
        )
        ProductSKU.objects.create(
            product=p,
            quantity=50,
            shipping_status='available',
            delivery_time="2-3 Days"
        )
    
    print("Creating Slider...")
    slide_url = upload_to_cloudinary("https://jkrintl.com/wp-content/uploads/2023/09/JKR9.9.jpg")
    HeroSlider.objects.create(
        title="Redefining Mobility",
        subtitle="Top-tier medical solutions",
        image_url=slide_url,
        is_active=True
    )

    print("Success! Database populated with DIRECT Cloudinary URLs in image_url fields.")

if __name__ == '__main__':
    populate()
