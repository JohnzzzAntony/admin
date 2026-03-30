from django.db import models
from ckeditor.fields import RichTextField

class AboutUs(models.Model):
    title = models.CharField(max_length=255, default="About Us")
    heading = models.CharField(max_length=255, default="We craft solutions that enhance and Simplify Lives.")
    content = RichTextField()
    is_active = models.BooleanField(default=True)
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
    def get_thumb_url(self):
        if self.thumbnail_url: return self.thumbnail_url
        return self.thumbnail.url if self.thumbnail else "https://via.placeholder.com/400x250"

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
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES, unique=True)
    def __str__(self): return self.get_section_type_display()
    def get_img_url(self):
        if self.image_url: return self.image_url
        return self.image.url if self.image else "https://via.placeholder.com/600x400"

class Service(models.Model):
    title = models.CharField(max_length=255)
    icon = models.ImageField(
        upload_to="services/", 
        null=True, 
        blank=True,
        help_text="Service Icon. Recommended: 256x256px (Transparent PNG). Max 500KB."
    )
    icon_url = models.URLField(blank=True, null=True)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['order']
    def __str__(self): return self.title
    def get_icon_url(self):
        if self.icon_url: return self.icon_url
        return self.icon.url if self.icon else "https://via.placeholder.com/64"

class Counter(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=50, help_text="Example: 15, 100+, etc.")
    order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['order']
    def __str__(self): return f"{self.title}: {self.value}"

class WhyUsCard(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon_svg = models.TextField(help_text="SVG code for icon", blank=True)
    order = models.PositiveIntegerField(default=0)
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
    class Meta: ordering = ['order']
    def __str__(self): return self.title or f"Gallery Image {self.id}"
    def get_img_url(self):
        if self.image_url: return self.image_url
        return self.image.url if self.image else "https://via.placeholder.com/600x400"

class Partner(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(
        upload_to="partners/", 
        null=True, 
        blank=True,
        help_text="Brand Logo. Recommended: 400x400px (Transparent PNG). Max 500KB."
    )
    logo_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, help_text="Optional link to partner website")
    order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['order']
    def __str__(self): return self.name
    def get_logo_url(self):
        if self.logo_url: return self.logo_url
        return self.logo.url if self.logo else "https://via.placeholder.com/200x80"
