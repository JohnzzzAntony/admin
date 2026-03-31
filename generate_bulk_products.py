import csv
import random

# Realistic Unsplash Image Bank
IMG_BANK = [
    "https://images.unsplash.com/photo-1516549655169-df83a0774514", # Lab
    "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b", # Pills
    "https://images.unsplash.com/photo-1576091160550-217359f4ecf8", # Equip
    "https://images.unsplash.com/photo-1584036561566-baf8f5f1b144", # Masks
    "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae", # FirstAid
    "https://images.unsplash.com/photo-1581594693702-fbdc51b2ad46", # MedBag
    "https://images.unsplash.com/photo-1550624559-4bae04422ddc", # Stethoscope
    "https://images.unsplash.com/photo-1612349317150-e413f289d05e", # LabCoat
    "https://images.unsplash.com/photo-1631815541542-e5510659359e", # Hospital
    "https://images.unsplash.com/photo-1631549916768-4119cb21fa04", # Thermometer
]

CATEGORIES = {
    "Medical Equipment": "https://images.unsplash.com/photo-1516549655169-df83a0774514",
    "Consumables": "https://images.unsplash.com/photo-1584036561566-baf8f5f1b144",
    "Diagnostic Tools": "https://images.unsplash.com/photo-1550624559-4bae04422ddc",
    "Surgical Supplies": "https://images.unsplash.com/photo-1581594693702-fbdc51b2ad46",
    "Laboratory": "https://images.unsplash.com/photo-1612349317150-e413f289d05e",
    "Home Care": "https://images.unsplash.com/photo-1631549916768-4119cb21fa04"
}

PREFIXES = ["Ultra", "Smart", "Compact", "Pro", "Eco", "Elite", "Advanced", "Precision"]
BASES = ["Sterilizer", "Inhaler", "Analyzer", "Compressor", "Cart", "Dispenser", "Light", "Ventilator"]

filename = "c:/Users/johns/Music/Pro/final_500_unified_import.csv"
header = [
    "category", "category_image_url", "name", "slug", "image_url", "gallery_image_urls",
    "features", "overview", "technical_info", "regular_price", "sale_price", "is_active", 
    "meta_title", "meta_description", "meta_keywords",
    "sku_title", "sku_id", "sku_quantity", "sku_shipping_status", "sku_weight"
]

with open(filename, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    
    for i in range(1, 501):
        cat_name = random.choice(list(CATEGORIES.keys()))
        cat_img = f"{CATEGORIES[cat_name]}?auto=format&fit=crop&q=80&w=600"
        
        prod_base = random.choice(BASES)
        name = f"JKR {random.choice(PREFIXES)} {prod_base} Model-{i:04d}"
        slug = f"jkr-{name.lower().replace(' ', '-')}-{i}"
        
        # Main Image
        main_img = f"{random.choice(IMG_BANK)}?auto=format&fit=crop&q=80&w=800"
        
        # Gallery (2-3 additional images)
        gallery = ",".join([
            f"{random.choice(IMG_BANK)}?auto=format&fit=crop&q=80&w=800"
            for _ in range(random.randint(2, 3))
        ])
        
        feat = "CE Certified\nISO Standard\nHigh Durability"
        overview = f"The {name} represents the pinnacle of {cat_name} technology, offering unmatched reliability."
        tech = f"Dimensions: {random.randint(20, 100)}x{random.randint(20, 100)}cm\nVoltage: 110-240V\nWarranty: 2 Years"
        
        reg = random.randint(50, 10000)
        sale = round(reg * 0.9, 2)
        
        m_title = f"{name} | Buy Professional {prod_base} Online"
        m_desc = f"Looking for {name}? We offer the best prices on {cat_name} in the UAE. Fast delivery and warranty included."
        m_keys = f"{cat_name}, {prod_base}, JKR International, Buy Online"
        
        sku_id = f"JKR-PROD-{i:04d}-SKU"
        sku_qty = random.randint(5, 1000)
        
        writer.writerow([
            cat_name, cat_img, name, slug, main_img, gallery,
            feat, overview, tech, reg, sale, "TRUE",
            m_title, m_desc, m_keys,
            "Standard Package", sku_id, sku_qty, "available", 2.5
        ])

print(f"Generated {filename}")
