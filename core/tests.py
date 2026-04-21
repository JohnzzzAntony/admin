import pytest
from django.utils.text import slugify
from products.models import Category, Product, Brand, Offer
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
class TestProductModels:
    
    def test_category_slug_generation(self):
        category = Category.objects.create(name="Medical Equipment")
        assert category.slug == "medical-equipment"
        
    def test_product_sku_generation(self):
        category = Category.objects.create(name="Surgical")
        product = Product.objects.create(name="Scalpel X1", category=category)
        assert product.sku_id.startswith("SCALPEL-X1") or product.sku_id.startswith("PRO")
        assert len(product.sku_id) > 10

    def test_product_price_with_percentage_offer(self):
        category = Category.objects.create(name="Devices")
        product = Product.objects.create(
            name="Heart Monitor", 
            category=category, 
            regular_price=Decimal("1000.00")
        )
        
        # Create an offer
        now = timezone.now()
        offer = Offer.objects.create(
            name="Summer Sale",
            offer_type="percentage",
            discount_value=Decimal("20.00"),
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=1)
        )
        offer.products.add(product)
        
        price_info = product.get_best_price_info()
        assert price_info['final_price'] == Decimal("800.00")
        assert price_info['discount_percentage'] == 20

    def test_seo_metadata_fields(self):
        category = Category.objects.create(
            name="Dental",
            meta_title="Best Dental Tools",
            meta_description="High quality dental equipment in Dubai."
        )
        assert category.meta_title == "Best Dental Tools"
        assert "Dubai" in category.meta_description
