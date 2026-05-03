
import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv('DATABASE_URL')

def run():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    with open('products_fixed_skus.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Sort data by model to handle dependencies
    # Categories first, then Products, then others
    order = ['products.category', 'products.product', 'products.productimage', 'products.offer', 'products.collection']
    data.sort(key=lambda x: order.index(x['model']) if x['model'] in order else 99)
    
    print(f"Starting import of {len(data)} objects...")
    
    for i, obj in enumerate(data):
        model = obj['model']
        pk = obj['pk']
        fields = obj['fields']
        
        print(f"Processing {model} pk={pk} ({i}/{len(data)})...")

        if model == 'products.category':
            table = 'products_category'
        elif model == 'products.product':
            table = 'products_product'
        elif model == 'products.productimage':
            table = 'products_productimage'
        elif model == 'products.offer':
            table = 'products_offer'
        elif model == 'products.collection':
            table = 'products_collection'
        else:
            continue
            
        cols = []
        vals = []
        
        # Define fields that MUST NOT be NULL per model
        model_must_not_be_null = {
            'products.category': ['meta_title', 'meta_title_ar', 'meta_description', 'meta_description_ar', 'meta_keywords', 'meta_keywords_ar', 'description', 'icon_svg'],
            'products.product': ['meta_title', 'meta_title_ar', 'meta_description', 'meta_description_ar', 'meta_keywords', 'meta_keywords_ar', 'delivery_time', 'features'],
            'products.productimage': [],
            'products.offer': [],
            'products.collection': []
        }
        
        must_not_be_null = model_must_not_be_null.get(model, [])
        
        # Merge existing fields with missing required fields
        all_fields = fields.copy()
        for f in must_not_be_null:
            if f not in all_fields or all_fields[f] is None:
                all_fields[f] = ""
        
        for k, v in all_fields.items():
            if k == 'parent' or k == 'category' or k == 'product':
                k = f"{k}_id"
            
            cols.append(f'"{k}"')
            if isinstance(v, dict) or isinstance(v, list):
                vals.append(json.dumps(v))
            else:
                vals.append(v)
        
        cols.append('"id"')
        vals.append(pk)
        
        placeholders = ', '.join(['%s'] * len(vals))
        col_str = ', '.join(cols)
        
        query = f"INSERT INTO {table} ({col_str}) VALUES ({placeholders}) ON CONFLICT (id) DO UPDATE SET "
        updates = []
        for c in cols:
            if c != '"id"':
                updates.append(f"{c} = EXCLUDED.{c}")
        query += ', '.join(updates)
        
        try:
            cur.execute(query, vals)
            if i % 100 == 0:
                print(f"Processed {i} objects...")
                conn.commit()
        except Exception as e:
            print(f"Error on {model} pk={pk}: {e}")
            conn.rollback()
            
    conn.commit()
    print("Done!")

if __name__ == '__main__':
    run()
