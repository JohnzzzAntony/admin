from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactFormSubmission, NewsletterSubscriber
from pages.models import ContactPage

def contact(request):
    """View to handle both GET (display form) and POST (submit form)."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        try:
            ContactFormSubmission.objects.create(
                name=name, email=email, phone=phone, message=message
            )
            messages.success(request, "Thank you! Your message has been sent successfully.")
        except Exception:
            messages.error(request, "There was an error sending your message. Please try again.")
            
        return redirect('contact:contact')

    # GET request
    contact_settings = ContactPage.objects.first()
    if not contact_settings:
        # Create a dummy instance to avoid None attribute access in templates
        contact_settings = ContactPage()
        
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
