from django.db import models
from ckeditor.fields import RichTextField

class PageHero(models.Model):
    PAGE_CHOICES = (
        ('about', 'About Us'),
        ('products', 'Products'),
        ('services', 'Services'),
        ('gallery', 'Gallery'),
        ('stores', 'Stores'),
        ('blog', 'Blog'),
        ('contact', 'Contact Us'),
    )
    page = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
    hero_image = models.ImageField(
        upload_to="heroes/", 
        null=True, 
        blank=True,
        help_text="Recommended: 1920x600px. JPG, WEBP. Max 2MB."
    )
    hero_image_url = models.URLField(blank=True, null=True, help_text="Alternative external link for hero image.")
    title = models.CharField(max_length=255, blank=True, help_text="Main title on the hero section.")
    title_html = models.CharField(max_length=512, blank=True, help_text="HTML Title (e.g. Our <span class='italic text-primary'>Legacy</span>). If provided, overrides Title.")
    subtitle = models.TextField(blank=True, help_text="Subtitle or description below the title.")
    
    button_text = models.CharField(max_length=100, blank=True, help_text="Primary button text.")
    button_link = models.CharField(max_length=255, blank=True, help_text="Link for primary button.")
    button_2_text = models.CharField(max_length=100, blank=True, help_text="Secondary button text.")
    button_2_link = models.CharField(max_length=255, blank=True, help_text="Link for secondary button.")
    
    alignment = models.CharField(max_length=20, choices=(('center', 'Center'), ('left', 'Left'), ('right', 'Right')), default='center')
    is_active = models.BooleanField(default=True, verbose_name="Status", choices=((True, 'Active'), (False, 'Hidden')))
    
    # SEO Optimization
    meta_title = models.CharField(max_length=255, blank=True, null=True, help_text="SEO Title Tag. If empty, Page Title will be used.")
    meta_description = models.TextField(blank=True, null=True, help_text="SEO Meta Description.")
    meta_keywords = models.CharField(max_length=512, blank=True, null=True, help_text="SEO Keywords.")
    
    @property
    def get_image_url(self):
        try:
            if self.hero_image: return self.hero_image.url
            if self.hero_image_url: return self.hero_image_url
        except Exception: pass
        return "https://via.placeholder.com/1920x600"

    def __str__(self): return self.get_page_display()
    class Meta:
        verbose_name = "Page Hero Setting"
        verbose_name_plural = "Page Hero Settings"

class AboutUs(models.Model):
    title = models.CharField(max_length=255, default="About Us")
    heading = models.CharField(max_length=255, default="We craft solutions that enhance and Simplify Lives.")
    content = RichTextField()
    
    image = models.ImageField(upload_to="about/", null=True, blank=True, help_text="Primary image for the story section.")
    image_url = models.URLField(blank=True, null=True, help_text="External URL for primary image.")
    image_alt = models.CharField(max_length=255, blank=True, default="JKR Story Image")
    
    experience_value = models.CharField(max_length=20, default="12+", help_text="e.g. 12+, 500+")
    experience_label = models.CharField(max_length=100, default="Years of Trust")
    
    legacy_title = models.CharField(max_length=255, default="Our Legacy", help_text="Title for the About page hero section.")
    legacy_subtitle = models.TextField(default="Defining excellence in the international trade landscape for over a decade.", help_text="Subtitle for the About page hero section.")
    
    is_active = models.BooleanField(default=True, verbose_name="Status", choices=((True, 'Active'), (False, 'Removed')))
    def __str__(self): return f"{self.title} Settings"
    
    @property
    def get_image_url(self):
        try:
            if self.image: return self.image.url
            if self.image_url: return self.image_url
        except Exception: pass
        return "https://via.placeholder.com/800x1000"
    class Meta: verbose_name_plural = "About Us Settings"

class VideoCard(models.Model):
    about_us = models.ForeignKey(AboutUs, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=255, blank=True)
    video_url = models.URLField(help_text="Direct link to video file (mp4)")
    thumbnail = models.ImageField(
        upload_to="about/videos/", 
        null=True, 
        blank=True,
        help_text="Recommended: 800x450px. JPG, WEBP. Max 1MB."
    )
    thumbnail_url = models.URLField(blank=True, null=True, help_text="Alternative external link for thumbnail.")
    order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['order']
    @property
    def get_image_url(self):
        try:
            if self.thumbnail: return self.thumbnail.url
            if self.thumbnail_url: return self.thumbnail_url
        except Exception: pass
        return "https://via.placeholder.com/400x250"

class MissionVision(models.Model):
    SECTION_TYPES = (('mission', 'Mission'), ('vision', 'Vision'), ('values', 'Values'))
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(
        upload_to="pages/", 
        null=True, 
        blank=True,
        help_text="Recommended: 1200x800px. JPG, WEBP. Max 2MB."
    )
    image_url = models.URLField(blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True, null=True)
    icon_svg = models.TextField(blank=True, help_text="Paste SVG code here.")
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES, unique=True)
    is_active = models.BooleanField(default=True, verbose_name="Status", choices=((True, 'Active'), (False, 'Hidden')))
    def __str__(self): return self.get_section_type_display()
    @property
    def get_image_url(self):
        try:
            if self.image: return self.image.url
            if self.image_url: return self.image_url
        except Exception: pass
        return "https://via.placeholder.com/600x400"

class Service(models.Model):
    title = models.CharField(max_length=255)
    icon = models.ImageField(
        upload_to="services/", 
        null=True, 
        blank=True,
        help_text="Service Icon. Recommended: 256x256px (Transparent PNG). Max 500KB."
    )
    icon_url = models.URLField(blank=True, null=True)
    icon_svg = models.TextField(blank=True, help_text="Paste SVG code here. If provided, it will be used instead of the image/URL.")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, verbose_name="Status", choices=((True, 'Active'), (False, 'Removed')))
    
    # SEO Optimization
    meta_title = models.CharField(max_length=255, blank=True, null=True, help_text="SEO Title Tag. If empty, Service Title will be used.")
    meta_description = models.TextField(blank=True, null=True, help_text="SEO Meta Description.")
    meta_keywords = models.CharField(max_length=512, blank=True, null=True, help_text="SEO Keywords (comma separated).")
    
    class Meta: ordering = ['order']
    def __str__(self): return self.title
    @property
    def get_image_url(self):
        try:
            if self.icon: return self.icon.url
            if self.icon_url: return self.icon_url
        except Exception: pass
        return "https://via.placeholder.com/64"

class Counter(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=50, help_text="Example: 15, 100+, etc.")
    icon_svg = models.TextField(blank=True, help_text="Paste SVG code here.")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, verbose_name="Status", choices=((True, 'Active'), (False, 'Removed')))
    class Meta: ordering = ['order']
    def __str__(self): return f"{self.title}: {self.value}"

class WhyUsCard(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon_svg = models.TextField(help_text="SVG code for icon", blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, verbose_name="Status", choices=((True, 'Active'), (False, 'Removed')))
    class Meta: ordering = ['order']
    def __str__(self): return self.title

class GalleryItem(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        upload_to="gallery/", 
        null=True, 
        blank=True,
        help_text="Recommended: 1000x1000px or 1200x800px. JPG, WEBP. Max 2MB."
    )
    image_url = models.URLField(blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True, null=True, help_text="SEO Alt Text")
    category = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, verbose_name="Status", choices=((True, 'Active'), (False, 'Removed')))
    class Meta: ordering = ['order']
    def __str__(self): return self.title or f"Gallery Image {self.id}"
    @property
    def get_image_url(self):
        try:
            if self.image: return self.image.url
            if self.image_url: return self.image_url
        except Exception: pass
        return "https://via.placeholder.com/600x400"

class Partner(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(
        upload_to="partners/", 
        null=True, 
        blank=True,
        help_text="Brand Logo. Recommended: 400x400px (Transparent PNG). Max 500KB."
    )
    logo_url = models.URLField(blank=True, null=True)
    logo_alt = models.CharField(max_length=255, blank=True, null=True)
    icon_svg = models.TextField(blank=True, help_text="Paste SVG logo code here. Used if provided.")
    website_url = models.URLField(blank=True, help_text="Optional link to partner website")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, verbose_name="Status", choices=((True, 'Active'), (False, 'Removed')))
    class Meta: ordering = ['order']
    def __str__(self): return self.name
    @property
    def get_image_url(self):
        try:
            if self.logo: return self.logo.url
            if self.logo_url: return self.logo_url
        except Exception: pass
        return "https://via.placeholder.com/200x80"

class ContactPage(models.Model):
    badge = models.CharField(max_length=100, default="Get in Touch")
    heading_html = models.CharField(max_length=512, default="Let's Start a <span class='italic text-primary'>Conversation</span>")
    subtitle = models.TextField(default="We are here to provide excellence and support for your every inquiry.")
    
    hours_label = models.CharField(max_length=100, default="Monday - Friday")
    hours_value = models.CharField(max_length=100, default="08:30 AM — 05:00 PM")
    
    form_title_html = models.CharField(max_length=512, default="Have a <span class='italic text-primary'>Question?</span>")
    form_subtitle = models.TextField(default="Send us a message and our specialists will reach out to you within 24 business hours.")
    
    support_image = models.ImageField(upload_to="contact/", null=True, blank=True)
    support_image_url = models.URLField(blank=True, null=True)
    
    def __str__(self): return "Contact Page Settings"
    @property
    def get_support_image(self):
        try:
            if self.support_image: return self.support_image.url
            if self.support_image_url: return self.support_image_url
        except Exception: pass
        return "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?q=80&w=2070"
    class Meta: verbose_name_plural = "Contact Page Settings"
