from django.contrib import admin
from .models import Post
from django.utils.html import format_html

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at', 'image_tag')
    list_filter = ('is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'excerpt')
    
    # We remove problematic fields from list_display if they exist.
    # We also keep fieldsets simple.
    fieldsets = (
        ('Article Details', {
            'fields': ('title', 'slug', 'featured_image', 'is_published')
        }),
        ('Content', {
            'fields': ('excerpt', 'content')
        }),
    )

    def image_tag(self, obj):
        try:
            if obj.featured_image:
                return format_html('<img src="{}" style="width: 60px; height:45px; object-fit: cover; border-radius: 4px;" />', obj.featured_image.url)
        except Exception:
            pass
        return "-"
    image_tag.short_description = 'Preview'
