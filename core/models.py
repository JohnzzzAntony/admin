from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=255, default="Demo International")
    logo = models.ImageField(
        upload_to="settings/", 
        null=True, 
        blank=True,
        help_text="Primary Brand Logo. Recommended: 500x120px (Transparent PNG). Max 1MB."
    )
    logo_url = models.URLField(blank=True, null=True)
    favicon = models.ImageField(
        upload_to="settings/", 
        null=True, 
        blank=True,
        help_text="Browser Icon. Recommended: 32x32px or 64x64px. ICO or PNG."
    )
    favicon_url = models.URLField(blank=True, null=True)
    fav_text = models.CharField(max_length=50, default="Demo", help_text="Small text shown near favicon or in tab.")
    
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    branch1_name = models.CharField(max_length=100, default="Dubai")
    dubai_address = models.TextField(blank=True, verbose_name="Branch 1 Address")
    branch2_name = models.CharField(max_length=100, default="Abu Dhabi")
    abudhabi_address = models.TextField(blank=True, verbose_name="Branch 2 Address")
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram_handle = models.CharField(max_length=100, default="@demo_intl", blank=True)
    
    
    
    
    

    
    # ── Footer Settings ───────────────────────────────────────────────────
    footer_quick_links_title = models.CharField(max_length=100, default="Quick Links")
    footer_support_title = models.CharField(max_length=100, default="Support")
    footer_legal_title = models.CharField(max_length=100, default="Legal")
    footer_newsletter_title = models.CharField(max_length=255, default="Subscribe to our Newsletter")
    footer_copyright_text = models.CharField(max_length=255, default="All rights reserved.", blank=True)
    
    # ── Notification Settings ───────────────────────────────────────────────
    enable_email_notifications    = models.BooleanField(default=True, verbose_name="Enable Email Notifications")
    enable_sms_notifications      = models.BooleanField(default=False, verbose_name="Enable SMS Notifications")
    enable_whatsapp_notifications = models.BooleanField(default=False, verbose_name="Enable WhatsApp Notifications")



    def get_logo_url(self):
        if self.logo_url: return self.logo_url
        return self.logo.url if self.logo else "/static/assets/logo.png"

    def __str__(self): return "Global Site Settings"
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    image = models.ImageField(
        upload_to="testimonials/", 
        null=True, 
        blank=True,
        help_text="Client Photo. Recommended: 200x200px (1:1). JPG, PNG. Max 500KB."
    )
    image_url = models.URLField(blank=True, null=True)
    rating = models.PositiveIntegerField(default=5)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    class Meta: ordering = ['order']
    def __str__(self): return f"Testimonial from {self.client_name}"
    def get_img_url(self):
        if self.image_url: return self.image_url
        return self.image.url if self.image else "https://via.placeholder.com/100"

class Client(models.Model):
    CATEGORY_CHOICES = (('Public', 'Public Sector'), ('Private', 'Private Sector'))
    name = models.CharField(max_length=100)
    logo = models.ImageField(
        upload_to="clients/", 
        null=True, 
        blank=True,
        help_text="Client Logo. Recommended: 300x120px (Transparent PNG). Max 500KB."
    )
    logo_url = models.URLField(blank=True, null=True)
    icon_svg = models.TextField(blank=True, help_text="Paste SVG code for logo here.")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='Public')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    class Meta: ordering = ['order']
    def __str__(self): return self.name
    def get_logo_url(self):
        if self.logo_url: return self.logo_url
        return self.logo.url if self.logo else "https://via.placeholder.com/150x60"

class SocialPost(models.Model):
    image = models.ImageField(
        upload_to="social/", 
        null=True, 
        blank=True,
        help_text="Instagram Preview. Recommended: 1080x1080px (Square). JPG, WEBP. Max 2MB."
    )
    image_url = models.URLField(blank=True, null=True)
    icon_svg = models.TextField(blank=True, help_text="Paste SVG code here.")
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['order']
    def get_img_url(self):
        if self.image_url: return self.image_url
        return self.image.url if self.image else "https://via.placeholder.com/400"

class StoreLocation(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to="stores/", 
        null=True, 
        blank=True,
        help_text="Storefront Photo. Recommended: 800x600px. JPG, WEBP. Max 1MB."
    )
    image_url = models.URLField(blank=True, null=True, help_text="Alternative: Direct link to an externally hosted image.")
    address = models.TextField()
    city = models.CharField(max_length=100, help_text="e.g. Dubai, Sharjah, Abu Dhabi")
    phone = models.CharField(max_length=50)
    map_url = models.URLField(verbose_name="Google Maps URL", help_text="Link to the location on Google Maps (Get Directions)")
    is_active = models.BooleanField(default=True, verbose_name="Enabled")
    order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")

    class Meta:
        ordering = ['order', 'name']

    def get_image_url(self):
        if self.image_url: return self.image_url
        return self.image.url if self.image else "https://via.placeholder.com/600x400"

    def __str__(self):
        return f"{self.name} ({self.city})"
