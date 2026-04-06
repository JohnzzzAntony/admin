from django.db import models

class DesignSettings(models.Model):
    # Colors
    primary_color = models.CharField(max_length=20, default="#114084", help_text="Hex code, e.g. #114084")
    secondary_color = models.CharField(max_length=20, default="#005CB9", help_text="Hex code, e.g. #005CB9")
    accent_glow_color = models.CharField(max_length=20, default="#0081ff", help_text="Color for ambient glow effects.")
    
    # Typography
    font_body = models.CharField(max_length=100, default="'Montserrat', sans-serif", help_text="CSS font-family value")
    font_heading = models.CharField(max_length=100, default="'Montserrat', sans-serif", help_text="CSS font-family value")
    
    # Visual Effects
    enable_glassmorphism = models.BooleanField(default=False, verbose_name="Enable Glassmorphism")
    enable_neumorphism = models.BooleanField(default=False, verbose_name="Enable Neumorphism")
    enable_ambient_glow = models.BooleanField(default=True, verbose_name="Enable Ambient Glow Background")
    enable_animations = models.BooleanField(default=True, verbose_name="Enable Scroll Animations (AOS)")
    
    # UI Components
    BUTTON_CHOICES = (
        ('pill', 'Pill (Fully Rounded)'),
        ('soft', 'Soft (8px Radius)'),
        ('sharp', 'Sharp (Square)'),
    )
    button_style = models.CharField(max_length=20, choices=BUTTON_CHOICES, default='pill')
    
    CARD_CHOICES = (
        ('standard', 'Standard Rounded'),
        ('glass', 'Glass Edge'),
        ('minimal', 'Minimalist (No Border)'),
    )
    card_style = models.CharField(max_length=20, choices=CARD_CHOICES, default='standard')
    
    LAYOUT_CHOICES = (
        ('boxed', 'Boxed Layout'),
        ('full', 'Full Width Layout'),
    )
    layout_style = models.CharField(max_length=20, choices=LAYOUT_CHOICES, default='full')
    dark_mode_enabled = models.BooleanField(default=False, verbose_name="Enable Dark Mode")

    # ── Header & Global Settings ──────────────────────────────────────────────
    header_title = models.CharField(max_length=255, default="Demo International")
    header_subtitle = models.CharField(max_length=255, default="Empowering Your Vision")
    
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
    hp_social_subtitle = models.CharField(max_length=255, default="Follow our Instagram @demo_intl")
    
    # ── Product Detail Settings ─────────────────────────────────────────────
    pd_related_title = models.CharField(max_length=255, default="Related Products")
    pd_show_related = models.BooleanField(default=True, verbose_name="Show Related Products")
    pd_related_count = models.PositiveIntegerField(default=4, verbose_name="Number of Related Products")

    # Advanced Animation Controls
    ANIMATION_EFFECTS = (
        ('fade-up', 'Fade Up'),
        ('fade-down', 'Fade Down'),
        ('zoom-in', 'Zoom In'),
        ('flip-left', 'Flip Left'),
        ('none', 'No Animation'),
    )
    global_animation_type = models.CharField(max_length=20, choices=ANIMATION_EFFECTS, default='fade-up')

    class Meta:
        verbose_name = "Design Configuration"
        verbose_name_plural = "Design Configuration"

    def __str__(self):
        return "Global Design Configuration"
