from django.contrib import admin
from .models import Post
from django.utils.html import format_html
from django.contrib import messages

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_tag', 'title', 'created_at')
    list_filter = ('created_at',)
    # prepopulated_fields = {'slug': ('title',)} # Removed as per user request for manual entry
    search_fields = ('title', 'content', 'excerpt')
    
    fieldsets = (
        ('Article Details', {
            'fields': ('title', 'slug', 'featured_image', 'featured_image_url')
        }),
        ('Content', {
            'fields': ('excerpt', 'content')
        }),
        ('SEO & Discovery', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
        }),
    )

    def image_tag(self, obj):
        url = obj.get_image_url
        if url:
            return format_html('<img src="{}" style="width: 60px; height:45px; object-fit: cover; border-radius: 4px;" />', url)
        return "-"
    image_tag.short_description = 'Preview'

    def save_model(self, request, obj, form, change):
        # Force published if no longer managed by checkbox
        obj.is_published = True
        super().save_model(request, obj, form, change)
        messages.success(request, f"📰 Blog post '{obj.title}' has been successfully published.")

    def delete_model(self, request, obj):
        title = obj.title
        super().delete_model(request, obj)
        messages.error(request, f"🗑️ Blog post '{title}' was deleted.")
