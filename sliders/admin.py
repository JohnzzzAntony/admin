from django.contrib import admin
from .models import HeroSlider, PromoBanner, BannerItem
from django.utils.html import format_html, mark_safe

from django.contrib import messages

@admin.register(HeroSlider)
class HeroSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview', 'order', 'is_active', 'button_text')
    list_editable = ('order', 'is_active')
    list_filter = ()
    radio_fields = {"is_active": admin.HORIZONTAL}

    def preview(self, obj):
        url = obj.get_bg_url()
        if url:
            return format_html('<img src="{}" style="width: 100px; height:60px; object-fit: cover; border-radius:4px;" />', url)
        elif obj.get_vid_url():
            return mark_safe('<span style="color: #6f42c1;">🎬 [Video Background]</span>')
        return "-"
    preview.short_description = 'Background Preview'

    fieldsets = (
        ('Header Information', {
            'fields': (('title', 'subtitle'), 'order'),
        }),
        ('Background Media', {
            'fields': (('image', 'image_url'), ('video', 'video_url')),
            'description': 'Upload a file or provide an external URL. Images are prioritized.'
        }),
        ('Action Layer', {
            'fields': (('button_text', 'button_link'),),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        messages.success(request, f"✨ Slider banner '{obj.title}' has been successfully saved.")

    def delete_model(self, request, obj):
        title = obj.title
        super().delete_model(request, obj)
        messages.error(request, f"🗑️ Slider banner '{title}' was deleted.")

class BannerItemInline(admin.StackedInline):
    model = BannerItem
    extra = 1
    fieldsets = (
        (None, {
            'fields': (
                ('image', 'image_url'),
                ('title', 'subtitle'),
                ('link', 'order'),
                'preview',
            )
        }),
    )
    readonly_fields = ('preview',)
    
    def preview(self, obj):
        url = obj.get_image_url
        if url:
            return format_html('<img src="{}" style="width: 100px; height:60px; object-fit: cover; border-radius:4px;" />', url)
        return "-"

@admin.register(PromoBanner)
class PromoBannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'layout', 'shape', 'homepage_order', 'is_active')
    list_editable = ('homepage_order', 'is_active')
    inlines = [BannerItemInline]
    radio_fields = {"is_active": admin.HORIZONTAL}
    
    fieldsets = (
        ('Section Overview', {
            'fields': (('name', 'homepage_order'), 'is_active'),
        }),
        ('Design & Layout', {
            'fields': (('layout', 'shape'),),
            'description': 'Select how the banners are arranged and their visual shape.'
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        messages.success(request, f"✨ Promo Section '{obj.name}' updated successfully.")
