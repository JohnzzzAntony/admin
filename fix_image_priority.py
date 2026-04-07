import re

file_path = 'products/models.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix priority in get_image_url for Product and ProductImage
# We look for the pattern:
# if self.image_url: return self.image_url
# if self.image: return self.image.url

old_block = r"(if self.image_url: return self.image_url\n\s+if self.image: return self.image.url)"
new_block = r"if self.image: return self.image.url\n            if self.image_url: return self.image_url"

# We use regex to handle both CRLF and LF
fixed_content = re.sub(
    r"if self\.image_url: return self\.image_url\r?\n\s+if self\.image: return self\.image\.url",
    r"if self.image: return self.image.url\n            if self.image_url: return self.image_url",
    content
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Successfully updated image priority logic in products/models.py")
