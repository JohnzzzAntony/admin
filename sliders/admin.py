from django.contrib import admin
from .models import HeroSlider
from django.utils.html import format_html

@admin.register(HeroSlider)
class HeroSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview', 'order', 'is_active', 'button_text')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)

    def preview(self, obj):
        url = obj.get_bg_url()
        if url:
            return format_html('<img src="{}" style="width: 100px; height:60px; object-fit: cover;" />', url)
        elif obj.get_vid_url():
            return format_html('<span style="color: blue;">[Video Background]</span>')
        return "-"
    preview.short_description = 'Background Preview'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'is_active', 'order')
        }),
        ('Media (Upload or External URL)', {
            'fields': (('image', 'image_url'), ('video', 'video_url'))
        }),
        ('Action Button', {
            'fields': ('button_text', 'button_link')
        }),
    )
