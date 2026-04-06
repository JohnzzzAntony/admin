from django.contrib import admin
from .models import SiteSettings, Testimonial, Client, SocialPost, StoreLocation
from .design_models import DesignSettings

@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('city', 'is_active')
    search_fields = ('name', 'address', 'city')
    fields = (('name', 'city'), 'address', ('phone', 'map_url'), ('image', 'image_url'), ('is_active', 'order'))

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name',)
    fieldsets = (
        ('Branding & Global', {
            'fields': (('site_name', 'fav_text'), ('logo', 'logo_url'), ('favicon', 'favicon_url'))
        }),
        ('SEO & Meta', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Communication', {
            'fields': (('email', 'phone'), 'whatsapp')
        }),
        ('Branch Addresses', {
            'fields': ('dubai_address', 'abudhabi_address')
        }),
        ('Footer Content', {
            'fields': (('footer_quick_links_title', 'footer_support_title'), ('footer_legal_title', 'footer_newsletter_title'), 'footer_copyright_text')
        }),
        ('Social Networking Links', {
            'fields': (('facebook', 'instagram'), ('linkedin', 'twitter', 'instagram_handle'))
        }),
        ('Notification Channels', {
            'fields': (
                'enable_email_notifications', 
                'enable_sms_notifications', 
                'enable_whatsapp_notifications'
            )
        }),
    )

@admin.register(DesignSettings)
class DesignSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'dark_mode_enabled', 'enable_glassmorphism', 'enable_ambient_glow')
    fieldsets = (
        ('Theme Colors', {
            'fields': (('primary_color', 'secondary_color', 'accent_glow_color'),),
            'description': 'Configure the global color palette. Accent glow is used for ambient background effects.'
        }),
        ('Typography', {
            'fields': (('font_body', 'font_heading'),),
            'description': 'Enter CSS font-family strings (e.g. "Google Font Name", sans-serif).'
        }),
        ('UI Styling Strategy', {
            'fields': (
                ('button_style', 'card_style', 'layout_style'),
            ),
            'description': 'Choose the shape of buttons, cards, and overall container layouts across the site.'
        }),
        ('Advanced Visual Effects', {
            'fields': (
                ('enable_glassmorphism', 'enable_neumorphism'),
                'enable_ambient_glow',
                ('enable_animations', 'global_animation_type'),
                'dark_mode_enabled'
            ),
            'description': 'Toggle premium visual techniques and AOS (Animate on Scroll) transitions.'
        }),
        ('Home Page Design & Titles', {
            'fields': (
                ('header_title', 'header_subtitle'),
                ('hp_collections_title', 'hp_collections_subtitle'),
                'hp_categories_title',
                ('hp_latest_products_title', 'hp_latest_products_subtitle'),
                'hp_latest_products_empty',
                ('hp_partners_title', 'hp_partners_subtitle'),
                ('hp_services_overtitle', 'hp_services_title'),
                'hp_services_subtitle',
                'hp_gallery_title',
                ('hp_testimonials_overtitle', 'hp_testimonials_title'),
                'hp_clients_title',
                ('hp_social_overtitle', 'hp_social_subtitle'),
            )
        }),
        ('Product Detail Page Design', {
            'fields': (('pd_related_title', 'pd_show_related'), 'pd_related_count')
        }),
    )

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'position', 'rating', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fields = ('client_name', 'position', 'content', ('image', 'image_url'), 'rating', 'order', 'is_active')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'order')
    list_editable = ('category', 'is_active', 'order')
    list_filter = ('category', 'is_active')
    fields = ('name', ('logo', 'logo_url'), 'category', 'order', 'is_active')

@admin.register(SocialPost)
class SocialPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'order')
    list_editable = ('order',)
    fields = (('image', 'image_url'), 'link', 'order')
