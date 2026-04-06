from django.contrib import admin
from .models import PageHero, AboutUs, VideoCard, MissionVision, Service, Counter, WhyUsCard, GalleryItem, Partner
from django.utils.html import format_html

@admin.register(PageHero)
class PageHeroAdmin(admin.ModelAdmin):
    list_display = ('page', 'title', 'hero_preview')
    fields = ('page', ('hero_image', 'hero_image_url'), 'title', 'subtitle')
    
    def hero_preview(self, obj):
        url = obj.get_hero_url()
        return format_html('<img src="{}" style="height:50px; width: 120px; object-fit: cover; border-radius: 5px;" />', url) if url else "-"
    hero_preview.short_description = 'Hero Preview'

class VideoCardInline(admin.TabularInline):
    model = VideoCard
    extra = 1
    fields = ('title', 'video_url', 'thumbnail', 'thumbnail_url', 'order')

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    inlines = [VideoCardInline]
    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)

@admin.register(MissionVision)
class MissionVisionAdmin(admin.ModelAdmin):
    list_display = ('section_type', 'title')
    fields = ('section_type', 'title', 'content', ('image', 'image_url'), 'icon_svg')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'image_tag')
    list_editable = ('order',)
    fields = (('title', 'order'), ('icon', 'icon_url'), 'icon_svg', 'description')
    
    def image_tag(self, obj):
        url = obj.get_icon_url()
        return format_html('<img src="{}" style="width: 45px; height:45px; border-radius: 5px; object-fit: contain;" />', url) if url else "-"
    image_tag.short_description = 'Icon'

@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'order')
    list_editable = ('value', 'order')
    fields = (('title', 'value'), 'icon_svg', 'order')

@admin.register(WhyUsCard)
class WhyUsCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'image_tag')
    list_editable = ('order', 'category')
    fields = (('title', 'category', 'order'), ('image', 'image_url'))
    
    def image_tag(self, obj):
        url = obj.get_img_url()
        return format_html('<img src="{}" style="width: 60px; height:45px; border-radius: 5px; object-fit: cover;" />', url) if url else "-"
    image_tag.short_description = 'Image'

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url', 'order', 'image_tag')
    list_editable = ('order',)
    fields = (('name', 'order'), ('logo', 'logo_url'), 'icon_svg', 'website_url')

    def image_tag(self, obj):
        url = obj.get_logo_url()
        return format_html('<img src="{}" style="height:45px; object-fit:contain; max-width: 120px;" />', url) if url else "-"
    image_tag.short_description = 'Logo'
