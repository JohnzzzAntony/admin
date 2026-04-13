from django.contrib import admin
from .models import SiteSettings, Testimonial, Client, SocialPost, StoreLocation, AnnouncementBar, SearchIndex
from .design_models import DesignSettings

from django.contrib import messages

@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    list_display = ('preview', 'name', 'city', 'phone', 'is_active', 'order')
    list_display_links = ('preview', 'name')
    list_editable = ('is_active', 'order')
    list_filter = ('city', 'is_active')
    search_fields = ('name', 'address', 'city')

    def preview(self, obj):
        from django.utils.safestring import mark_safe
        return mark_safe(f'<img src="{obj.get_image_url}" width="50" height="35" style="object-fit:cover; border-radius:4px; border:1px solid #ddd;" />')
    preview.short_description = "Image"
    
    fieldsets = (
        ('Location Info', {
            'fields': (('name', 'city'), 'address', 'order'),
        }),
        ('Communication & Map', {
            'fields': (('phone', 'map_url'),),
        }),
        ('Branding Image', {
            'fields': (('image', 'image_url'),),
        }),
    )
    radio_fields = {"is_active": admin.HORIZONTAL}

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        messages.success(request, f"🚀 Store Location '{obj.name}' has been successfully saved.")

    def delete_model(self, request, obj):
        name = obj.name
        super().delete_model(request, obj)
        messages.error(request, f"🗑️ Store Location '{name}' was deleted.")

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name',)
    fieldsets = (
        ('Overview & Branding', {
            'fields': (('site_name', 'company_name'), ('fav_text', 'logo', 'logo_url'), ('favicon', 'favicon_url')),
            'description': 'Main site identification and logo assets.'
        }),
        ('SEO Presence', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
        ('Communication Channels', {
            'fields': (('email', 'phone', 'whatsapp'),),
        }),
        ('Physical Presence', {
            'fields': (('branch1_name', 'dubai_address'), ('branch2_name', 'abudhabi_address')),
        }),
        ('Footer & Notifications', {
            'fields': (('footer_quick_links_title', 'footer_support_title', 'footer_legal_title'), ('footer_newsletter_title', 'footer_copyright_text'), ('enable_email_notifications', 'enable_sms_notifications', 'enable_whatsapp_notifications')),
            'classes': ('collapse',),
        }),
        ('Social Links', {
            'fields': (('facebook', 'instagram', 'linkedin', 'twitter'), 'instagram_handle'),
            'classes': ('collapse',),
        }),
    )
    radio_fields = {
        "enable_email_notifications": admin.HORIZONTAL,
        "enable_sms_notifications": admin.HORIZONTAL,
        "enable_whatsapp_notifications": admin.HORIZONTAL,
    }

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        messages.success(request, "⚙️ Global site settings have been successfully updated.")

@admin.register(DesignSettings)
class DesignSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'dark_mode_enabled', 'enable_glassmorphism', 'enable_ambient_glow')
    fieldsets = (
        ('Color Palette', {
            'fields': (
                ('primary_color', 'secondary_color', 'accent_glow_color'),
                ('header_bg_color', 'footer_bg_color'),
            ),
            'description': 'Define the visual tone of your store. Use hex codes (e.g. #1a1a1a). Header and footer colors are applied site-wide.'
        }),
        ('Typography', {
            'fields': (('font_body', 'font_heading'),),
        }),
        ('UI Strategy', {
            'fields': (('button_style', 'card_style', 'layout_style'),),
        }),
        ('Special Visuals', {
            'fields': (
                ('enable_glassmorphism', 'enable_neumorphism', 'enable_ambient_glow'), 
                ('enable_animations', 'global_animation_type', 'dark_mode_enabled'),
                ('counter_animation_style', 'counter_animation_speed'),
            ),
            'description': 'Premium effects, dark mode, and counter animation controls.'
        }),
        ('Homepage Content Blocks', {
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
            ),
            'classes': ('collapse',),
        }),
        ('Product Display', {
            'fields': (('pd_related_title', 'pd_show_related', 'pd_related_count'),),
        }),
    )
    radio_fields = {
        "enable_glassmorphism": admin.HORIZONTAL,
        "enable_neumorphism": admin.HORIZONTAL,
        "enable_ambient_glow": admin.HORIZONTAL,
        "enable_animations": admin.HORIZONTAL,
        "dark_mode_enabled": admin.HORIZONTAL,
        "pd_show_related": admin.HORIZONTAL,
        "counter_animation_style": admin.HORIZONTAL,
    }

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        messages.success(request, "🎨 Design settings have been successfully updated.")

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('preview', 'client_name', 'position', 'rating', 'is_active', 'order')
    list_display_links = ('preview', 'client_name')
    list_editable = ('is_active', 'order')
    radio_fields = {"is_active": admin.HORIZONTAL}
    list_filter = ('rating', 'is_active')

    def preview(self, obj):
        from django.utils.safestring import mark_safe
        return mark_safe(f'<img src="{obj.get_image_url}" width="40" height="40" style="border-radius:50%; object-fit:cover; border:1px solid #ddd;" />')
    preview.short_description = "Photo"
    
    fieldsets = (
        ('Client Profile', {
            'fields': (('client_name', 'position'), ('rating', 'order')),
        }),
        ('Content', {
            'fields': ('content',),
        }),
        ('Media', {
            'fields': (('image', 'image_url'),),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        messages.success(request, f"💬 Testimonial from '{obj.client_name}' has been saved.")

    def delete_model(self, request, obj):
        name = obj.client_name
        super().delete_model(request, obj)
        messages.error(request, f"🗑️ Testimonial from '{name}' was deleted.")

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('preview', 'name', 'category', 'is_active', 'order')
    list_display_links = ('preview', 'name')
    list_editable = ('category', 'is_active', 'order')
    radio_fields = {"is_active": admin.HORIZONTAL}
    list_filter = ('category', 'is_active')

    def preview(self, obj):
        from django.utils.safestring import mark_safe
        return mark_safe(f'<img src="{obj.get_image_url}" width="60" height="30" style="object-fit:contain; border:1px solid #eee; padding:2px; background:#fff; border-radius:4px;" />')
    preview.short_description = "Logo"
    
    fieldsets = (
        ('Client Info', {
            'fields': (('name', 'category'), 'order'),
        }),
        ('Assets (Logo/Icon)', {
            'fields': (('logo', 'logo_url'), 'icon_svg'),
            'description': 'Provide either a traditional logo or a custom SVG path.'
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        messages.success(request, f"🤝 Client '{obj.name}' has been successfully saved.")

    def delete_model(self, request, obj):
        name = obj.name
        super().delete_model(request, obj)
        messages.error(request, f"🗑️ Client '{name}' was removed.")

@admin.register(SocialPost)
class SocialPostAdmin(admin.ModelAdmin):
    list_display = ('preview', 'link', 'order')
    list_display_links = ('preview', 'link')
    list_editable = ('order',)

    def preview(self, obj):
        from django.utils.safestring import mark_safe
        return mark_safe(f'<img src="{obj.get_image_url}" width="40" height="40" style="object-fit:cover; border-radius:4px; border:1px solid #ddd;" />')
    preview.short_description = "Preview"
    
    fieldsets = (
        ('Post Configuration', {
            'fields': (('link', 'order'),),
        }),
        ('Media Assets', {
            'fields': (('image', 'image_url'), 'icon_svg'),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        messages.success(request, "📸 Social post entry has been saved.")

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        messages.error(request, "🗑️ Social post entry was deleted.")

@admin.register(AnnouncementBar)
class AnnouncementBarAdmin(admin.ModelAdmin):
    list_display = ('text', 'start_date', 'end_date', 'closable', 'is_active')
    list_editable = ('is_active',)
    radio_fields = {"is_active": admin.HORIZONTAL, "closable": admin.HORIZONTAL}
    list_filter = ('is_active', 'closable')
    
    fieldsets = (
        ('Banner Message', {
            'fields': (('text', 'closable', 'is_active'),),
        }),
        ('Appearance', {
            'fields': (('background_color', 'text_color'),),
        }),
        ('Schedule', {
            'fields': (('start_date', 'end_date'),),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        messages.success(request, f"📢 Announcement '{obj.text[:30]}...' has been updated.")

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        messages.error(request, "🗑️ Announcement was removed.")

