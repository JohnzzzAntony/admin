
import json
with open('products_fixed_skus.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cats_with_parents = [obj for obj in data if obj['model'] == 'products.category' and obj['fields']['parent'] is not None]
print(f"Total categories with parents in JSON: {len(cats_with_parents)}")
for c in cats_with_parents[:20]:
    print(f"ID: {c['pk']} | Name: {c['fields']['name']} | ParentID: {c['fields']['parent']}")
