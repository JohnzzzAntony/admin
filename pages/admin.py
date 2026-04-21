from django.contrib import admin
from .models import PageHero, AboutUs, VideoCard, MissionVision, Service, Counter, WhyUsCard, GalleryItem, Partner, ContactPage
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
        ('SEO Optimization', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
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
        ('Cinematic Branding', {
            'fields': ('legacy_title', 'legacy_subtitle'),
        }),
        ('Experience Stats', {
            'fields': (('experience_value', 'experience_label'),),
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
        ('SEO Optimization', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
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
            ('Products', '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>'),
            ('Global', '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'),
            ('Awards', '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"/><circle cx="12" cy="8" r="6"/></svg>'),
            ('Delivery', '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 17h4V5H2v12h3"/><path d="M20 17h2v-3.34a4 4 0 0 0-1.17-2.83L17 7h-3"/><circle cx="7.5" cy="17.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>'),
            ('Trusted', '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'),
            ('Health', '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'),
            ('Care', '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>'),
            ('Location', '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'),
        ]
        
        # Stylesheet for the helper
        styles = """
            <style>
                .svg-helper-container { background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; font-family: inherit; }
                .svg-helper-title { margin: 0 0 15px 0; font-weight: bold; color: #475569; display: flex; align-items: center; gap: 8px; }
                .svg-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(105px, 1fr)); gap: 12px; }
                .svg-card { background: #fff; text-align: center; cursor: pointer; padding: 12px; border: 1px solid #e2e8f0; border-radius: 10px; transition: all 0.2s; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
                .svg-card:hover { border-color: #2563eb; background: #f1f5f9; transform: translateY(-2px); box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
                .svg-card-icon { color: #2563eb; margin-bottom: 8px; display: flex; justify-content: center; }
                .svg-card-name { font-size: 11px; color: #64748b; font-weight: 600; line-height: 1.2; display: block; }
                .svg-footer { margin-top: 20px; padding-top: 15px; border-top: 1px solid #e2e8f0; font-size: 13px; color: #64748b; }
                .svg-footer a { color: #2563eb; font-weight: bold; text-decoration: none; }
            </style>
        """

        html_parts = [styles, '<div class="svg-helper-container">']
        html_parts.append('<p class="svg-helper-title">✨ Quick Select Icons</p>')
        html_parts.append('<div class="svg-grid">')
        
        for name, code in icons:
            # Safely build each card
            card = format_html(
                '<div class="svg-card" onclick="document.getElementById(\'id_icon_svg\').value = \'{}\'; return false;">'
                '<div class="svg-card-icon">{}</div>'
                '<span class="svg-card-name">{}</span>'
                '</div>',
                code, 
                format_html('{}', code), 
                name
            )
            html_parts.append(card)
        
        html_parts.append('</div>')
        html_parts.append(
            '<div class="svg-footer">'
            'Need more? Visit <a href="https://lucide.dev/icons" target="_blank">Lucide Icons</a>, '
            'copy the "SVG" code, and paste it above.'
            '</div>'
        )
        html_parts.append('</div>')
        
        from django.utils.safestring import mark_safe
        return mark_safe(''.join(html_parts))
    svg_selection_helper.short_description = "Icon Selection Center"

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

@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'badge')
    fieldsets = (
        ('Hero Section', {
            'fields': ('badge', 'heading_html', 'subtitle'),
        }),
        ('Business Hours', {
            'fields': (('hours_label', 'hours_value'),),
        }),
        ('Inquiry Section', {
            'fields': ('form_title_html', 'form_subtitle', ('support_image', 'support_image_url')),
        }),
    )

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)
