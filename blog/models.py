from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    featured_image = models.ImageField(
        upload_to="blog/",
        help_text="Blog Cover. Recommended: 1200x800px. JPG, WEBP. Max 2MB."
    )
    excerpt = models.TextField(blank=True, help_text="Short description for the blog card on the listing page.")
    content = RichTextField()
    
    # Meta
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
