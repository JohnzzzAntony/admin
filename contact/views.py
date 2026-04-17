from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactFormSubmission, NewsletterSubscriber
from pages.models import ContactPage

def contact(request):
    """Image 2 redesign: Handles contact form submission from the new layout."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone') # Mapped from 'mobile' in frontend
        message = request.POST.get('message')
        
        ContactFormSubmission.objects.create(
            name=name, email=email, phone=phone, message=message
        )
        messages.success(request, "Hi! Thanks for reaching out. We will get back to you soon.")
        return redirect('contact:contact')

    contact_settings = ContactPage.objects.first()
    return render(request, 'contact/contact.html', {'contact_settings': contact_settings})

def subscribe(request):
    """Handles newsletter subscription from Image 1/2 footer."""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, "Thanks for subscribing to our newsletter!")
            else:
                messages.info(request, "You are already subscribed to our newsletter.")
    
    return redirect(request.META.get('HTTP_REFERER', '/'))
