from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=255, default="Demo Store")
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
    dubai_address = models.TextField(blank=True)
    abudhabi_address = models.TextField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram_handle = models.CharField(max_length=100, default="@demostore", blank=True)
    
    # ── Header & Global Settings ──────────────────────────────────────────────
    header_title = models.CharField(max_length=255, default="Demo Store")
    header_subtitle = models.CharField(max_length=255, default="PREMIUM QUALITY")
    
    # ── Homepage Section Titles ─────────────────────────────────────────────
    hp_collections_title = models.CharField(max_length=255, default='Exclusive <span class="text-primary">Collections</span>')
    hp_collections_subtitle = models.TextField(default='Handpicked selection of premium medical equipment and essential supplies.', blank=True)
    
    hp_categories_title = models.CharField(max_length=255, default='Product <span class="text-primary">Categories</span>')
    
    hp_latest_products_title = models.CharField(max_length=255, default='Explore <span class="text-primary">Latest Products</span>')
    hp_latest_products_subtitle = models.TextField(default='Discover our newest medical innovations and technology.', blank=True)
    hp_latest_products_empty = models.CharField(max_length=255, default='Stay tuned for our latest medical products.', blank=True)
    
    hp_partners_title = models.CharField(max_length=255, default="We Deal with,")
    hp_partners_subtitle = models.TextField(default="100+ partnerships we've made ensure the quality of products we distribute", blank=True)
    
    hp_services_overtitle = models.CharField(max_length=255, default="OUR SERVICES")
    hp_services_title = models.CharField(max_length=255, default="Specialized Maintenance Services")
    hp_services_subtitle = models.TextField(default="We are dedicated to maintaining the health and effectiveness of your essential diagnostic equipment.", blank=True)
    
    hp_gallery_title = models.CharField(max_length=255, default='Latest <span class="text-primary">Gallery & Updates</span>')
    
    hp_testimonials_overtitle = models.CharField(max_length=255, default="TESTIMONIALS")
    hp_testimonials_title = models.CharField(max_length=255, default="Read what our clients have to share!")
    
    hp_clients_title = models.CharField(max_length=255, default="Our Clients")
    
    hp_social_overtitle = models.CharField(max_length=255, default="GO SOCIAL WITH US")
    hp_social_subtitle = models.CharField(max_length=255, default="Follow our Instagram @jkrinternational")

    # ── Product Detail Settings ─────────────────────────────────────────────
    pd_related_title = models.CharField(max_length=255, default="Related Products")
    pd_show_related = models.BooleanField(default=True, verbose_name="Show Related Products")
    pd_related_count = models.PositiveIntegerField(default=4, verbose_name="Number of Related Products")
    
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


class FrontendDesign(models.Model):
    # Colors
    primary_color = models.CharField(max_length=20, default="#114084", help_text="Main brand color (Buttons, Headlines)")
    secondary_color = models.CharField(max_length=20, default="#3498db", help_text="Secondary actions and accents")
    accent_color = models.CharField(max_length=20, default="#2271b1", help_text="Hover states and links")
    bg_light = models.CharField(max_length=20, default="#f8f9fa", help_text="Light mode background")
    bg_dark = models.CharField(max_length=20, default="#121212", help_text="Dark mode background")
    text_main = models.CharField(max_length=20, default="#1a1a1a", help_text="Primary text color")
    text_muted = models.CharField(max_length=20, default="#6c757d", help_text="Secondary/muted text")

    # Typography
    body_font_family = models.CharField(max_length=255, default="'Outfit', sans-serif", help_text="Main body text font")
    heading_font_family = models.CharField(max_length=255, default="'Outfit', sans-serif", help_text="Headline font")
    base_font_size = models.PositiveIntegerField(default=16, help_text="Base font size in px")

    # Component Styles
    border_radius = models.CharField(max_length=20, default="16px", help_text="Radius for cards, buttons, images")
    button_style = models.CharField(max_length=20, choices=(('square', 'Square'), ('rounded', 'Rounded'), ('pill', 'Pill')), default='pill')
    card_shadow = models.CharField(max_length=100, default="0 8px 30px rgba(0,0,0,0.08)", help_text="CSS shadow for cards")
    glassmorphism = models.BooleanField(default=True, help_text="Enable glass effects for headers and cards")

    # Motion & Animation
    enable_aos = models.BooleanField(default=True, verbose_name="Enable Scroll Animations")
    animation_duration = models.PositiveIntegerField(default=800, help_text="Default AOS duration in ms")
    page_transitions = models.BooleanField(default=True, help_text="Enable smooth page fade-in")

    # UI State
    dark_mode_default = models.BooleanField(default=False, verbose_name="Default to Dark Mode")

    def __str__(self): return "Live Frontend Design Configuration"

    class Meta:
        verbose_name = "Frontend Design Control"
        verbose_name_plural = "Frontend Design Control"
