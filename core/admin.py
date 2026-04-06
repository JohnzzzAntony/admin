from django.contrib import admin
from .models import SiteSettings, Testimonial, Client, SocialPost, StoreLocation, FrontendDesign

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
            'fields': (('site_name', 'fav_text'), ('logo', 'logo_url'), ('favicon', 'favicon_url'), ('header_title', 'header_subtitle'))
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
        ('Home Page - Collections', {
            'fields': ('hp_collections_title', 'hp_collections_subtitle')
        }),
        ('Home Page - Categories', {
            'fields': ('hp_categories_title',)
        }),
        ('Home Page - Latest Products', {
            'fields': ('hp_latest_products_title', 'hp_latest_products_subtitle', 'hp_latest_products_empty')
        }),
        ('Home Page - Partners', {
            'fields': ('hp_partners_title', 'hp_partners_subtitle')
        }),
        ('Home Page - Services', {
            'fields': ('hp_services_overtitle', 'hp_services_title', 'hp_services_subtitle')
        }),
        ('Home Page - Gallery', {
            'fields': ('hp_gallery_title',)
        }),
        ('Home Page - Testimonials', {
            'fields': ('hp_testimonials_overtitle', 'hp_testimonials_title')
        }),
        ('Home Page - Clients', {
            'fields': ('hp_clients_title',)
        }),
        ('Home Page - Social', {
            'fields': ('hp_social_overtitle', 'hp_social_subtitle')
        }),
        ('Product Detail Page', {
            'fields': (('pd_related_title', 'pd_show_related'), 'pd_related_count')
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


@admin.register(FrontendDesign)
class FrontendDesignAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    fieldsets = (
        ('Theme Colors', {
            'fields': (('primary_color', 'secondary_color', 'accent_color'), ('bg_light', 'bg_dark'), ('text_main', 'text_muted'))
        }),
        ('Typography', {
            'fields': (('body_font_family', 'heading_font_family'), 'base_font_size')
        }),
        ('Component Styles', {
            'fields': (('border_radius', 'button_style'), 'card_shadow', 'glassmorphism')
        }),
        ('Motion & Animation', {
            'fields': (('enable_aos', 'animation_duration'), 'page_transitions')
        }),
        ('UI State', {
            'fields': ('dark_mode_default',)
        }),
    )

    def has_add_permission(self, request):
        # Only allow one configuration object
        return not FrontendDesign.objects.exists()
