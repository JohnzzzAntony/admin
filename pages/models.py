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
    subtitle = models.TextField(blank=True, help_text="Subtitle or description below the title.")
    
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
    is_active = models.BooleanField(default=True, verbose_name="Status", choices=((True, 'Active'), (False, 'Removed')))
    def __str__(self): return f"{self.title} Settings"
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
    icon_svg = models.TextField(blank=True, help_text="Paste SVG code here.")
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES, unique=True)
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
