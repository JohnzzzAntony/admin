from django.contrib import admin
from .models import PageHero, AboutUs, VideoCard, MissionVision, Service, Counter, WhyUsCard, GalleryItem, Partner
from django.utils.html import format_html

@admin.register(PageHero)
class PageHeroAdmin(admin.ModelAdmin):
    list_display = ('page', 'title', 'hero_preview')
    readonly_fields = ('hero_preview',)
    
    fieldsets = (
        ('Reference', {
            'fields': ('page',),
        }),
        ('Hero Identity', {
            'fields': (('title', 'subtitle'),),
        }),
        ('Imagery', {
            'fields': (('hero_image', 'hero_image_url'),),
        }),
    )
    
    def hero_preview(self, obj):
        url = obj.get_image_url
        return format_html('<img src="{}" style="height:50px; width: 120px; object-fit: cover; border-radius: 5px;" />', url) if url else "-"
    hero_preview.short_description = 'Hero Preview'

class VideoCardInline(admin.TabularInline):
    model = VideoCard
    extra = 0
    fields = ('title', 'video_url', ('thumbnail', 'thumbnail_url'), 'order')

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    inlines = [VideoCardInline]
    
    radio_fields = {"is_active": admin.HORIZONTAL}
    
    fieldsets = (
        ('Brand Story', {
            'fields': (('title', 'heading'), 'is_active', 'content'),
        }),
    )

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)

@admin.register(MissionVision)
class MissionVisionAdmin(admin.ModelAdmin):
    list_display = ('section_type', 'title')
    
    fieldsets = (
        ('Strategic Goal', {
            'fields': (('section_type', 'title'),),
        }),
        ('Content & Visuals', {
            'fields': ('content', ('image', 'image_url'), 'icon_svg'),
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'image_tag')
    list_editable = ('order', 'is_active')
    radio_fields = {"is_active": admin.HORIZONTAL}
    
    fieldsets = (
        ('Service Info', {
            'fields': (('title', 'order'), 'is_active'),
        }),
        ('Appearance', {
            'fields': (('icon', 'icon_url'), 'icon_svg'),
        }),
        ('Narrative', {
            'fields': ('description',),
        }),
    )
    
    def image_tag(self, obj):
        url = obj.get_image_url
        return format_html('<img src="{}" style="width: 45px; height:45px; border-radius: 5px; object-fit: contain;" />', url) if url else "-"
    image_tag.short_description = 'Icon'

@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'order', 'is_active')
    list_editable = ('value', 'order', 'is_active')
    radio_fields = {"is_active": admin.HORIZONTAL}
    
    fieldsets = (
        ('Statistic', {
            'fields': (('title', 'value'), 'is_active'),
        }),
        ('Configuration', {
            'fields': ('icon_svg', 'order', 'svg_selection_helper'),
            'description': 'Paste an SVG code into the field above. You can use the quick-copy list below for common icons.'
        }),
    )
    readonly_fields = ('svg_selection_helper',)

    def svg_selection_helper(self, obj):
        icons = [
            ('Happy Clients', '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'),
            ('Experience', '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>'),
            ('Total Products', '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>'),
            ('Global Reach', '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'),
            ('Awards Won', '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"/><circle cx="12" cy="8" r="6"/></svg>'),
            ('Quick Delivery', '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 17h4V5H2v12h3"/><path d="M20 17h2v-3.34a4 4 0 0 0-1.17-2.83L17 7h-3"/><circle cx="7.5" cy="17.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>'),
        ]
        
        html = '<div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 10px;">'
        for name, code in icons:
            # Inline JS to copy to textarea
            click_js = f"document.getElementById('id_icon_svg').value = `{code}`; return false;"
            html += f"""
                <div style="text-align: center; cursor: pointer; padding: 10px; border: 1px solid #ddd; border-radius: 8px; width: 80px;" onclick="{click_js}">
                    <div style="color: var(--primary-blue, #2563eb); margin-bottom: 5px;">{code}</div>
                    <span style="font-size: 10px; color: #666; display: block; line-height: 1.1;">{name}</span>
                </div>
            """
        html += '</div>'
        return format_html(html)
    svg_selection_helper.short_description = "Common Icons (Click to select)"

@admin.register(WhyUsCard)
class WhyUsCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    radio_fields = {"is_active": admin.HORIZONTAL}
    
    fieldsets = (
        ('Advantage Card', {
            'fields': (('title', 'order'), 'is_active', 'description', 'icon_svg'),
        }),
    )

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'is_active', 'image_tag')
    list_editable = ('order', 'category', 'is_active')
    radio_fields = {"is_active": admin.HORIZONTAL}
    
    fieldsets = (
        ('Metadata', {
            'fields': (('title', 'category', 'order'), 'is_active'),
        }),
        ('Asset', {
            'fields': (('image', 'image_url'),),
        }),
    )
    
    def image_tag(self, obj):
        url = obj.get_image_url
        return format_html('<img src="{}" style="width: 60px; height:45px; border-radius: 5px; object-fit: cover;" />', url) if url else "-"
    image_tag.short_description = 'Image'

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url', 'order', 'is_active', 'image_tag')
    list_editable = ('order', 'is_active')
    radio_fields = {"is_active": admin.HORIZONTAL}
    
    fieldsets = (
        ('Company Details', {
            'fields': (('name', 'order'), 'is_active', 'website_url'),
        }),
        ('Branding', {
            'fields': (('logo', 'logo_url'), 'icon_svg'),
        }),
    )

    def image_tag(self, obj):
        url = obj.get_image_url
        return format_html('<img src="{}" style="height:45px; object-fit:contain; max-width: 120px;" />', url) if url else "-"
    image_tag.short_description = 'Logo'
