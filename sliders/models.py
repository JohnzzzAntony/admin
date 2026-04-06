from django.db import models

class HeroSlider(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        upload_to="sliders/", 
        null=True, 
        blank=True,
        help_text="Desktop slider image. Recommended: 1920x800px. JPG, WEBP. Max 2MB."
    )
    image_url = models.URLField(blank=True, null=True, help_text="External URL for background image.")
    video = models.FileField(
        upload_to="sliders/videos/", 
        null=True, 
        blank=True,
        help_text="Background video. Recommended: MP4 format. Max 5MB for performance."
    )
    video_url = models.URLField(blank=True, null=True, help_text="External URL for background video (YouTube/Vimeo not supported for direct background).")
    
    button_text = models.CharField(max_length=100, default="Enquire Now")
    button_link = models.CharField(max_length=255, default="/contact-us/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def get_bg_url(self):
        if self.image_url: return self.image_url
        return self.image.url if self.image else ""

    def get_vid_url(self):
        if self.video_url: return self.video_url
        return self.video.url if self.video else ""

    def __str__(self): return self.title
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Hero Sliders"
