from django.contrib import admin
from .models import ContactFormSubmission, NewsletterSubscriber

@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    search_fields = ('name', 'email', 'phone', 'subject', 'message')
    
    fieldsets = (
        ('Contact Info', {
            'fields': (('name', 'email', 'phone'),)
        }),
        ('Message details', {
            'fields': ('subject', 'message', 'is_read', 'created_at')
        }),
    )

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
