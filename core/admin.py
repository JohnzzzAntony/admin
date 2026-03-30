from django.contrib import admin
from .models import SiteSettings, NavMenuItem, Testimonial, Client, SocialPost

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name',)
    fieldsets = (
        ('Branding', {
            'fields': (('site_name', 'logo', 'logo_url'), ('favicon', 'favicon_url'))
        }),
        ('SEO & Meta', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Communication', {
            'fields': (('email', 'phone'), 'whatsapp')
        }),
        ('Branches', {
            'fields': ('dubai_address', 'abudhabi_address')
        }),
        ('Social Networking', {
            'fields': (('facebook', 'instagram'), ('linkedin', 'twitter', 'instagram_handle'))
        }),
    )

@admin.register(NavMenuItem)
class NavMenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'order', 'is_active')
    list_editable = ('order', 'is_active')

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
