from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Your account has been created.")
            return redirect('core:home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                # Redirect to next page if it exists
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('core:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    next_url = request.GET.get('next')
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('core:home')

def guest_checkout_view(request):
    """Allows users to proceed to checkout without an account."""
    next_url = request.GET.get('next', 'orders:checkout')
    # If the user is already logged in, just redirect to next
    if request.user.is_authenticated:
        return redirect(next_url)
    
    request.session['is_guest_checkout'] = True
    return redirect(next_url)

# --- Social Auth with Supabase ---
from core.supabase_client import supabase
from django.contrib.auth.models import User
from django.conf import settings

def social_login(request, provider):
    """
    Initiate a social login via Supabase.
    Redirects user to the social provider's login page.
    """
    # Build the full callback URL for your local or live site
    redirect_to = request.build_absolute_uri('/accounts/callback/')
    
    # Generate the OAuth login URL
    result = supabase.auth.get_oauth_url(
        provider=provider,
        redirect_to=redirect_to
    )
    
    # Supabase SDK returns a dictionary or object with the URL
    # or sometimes just the URL string depending on version. 
    # Usually it's in result.url
    if hasattr(result, 'url'):
        return redirect(result.url)
        
    return redirect('accounts:login')

def social_callback(request):
    """
    Handles the return logic from Supabase.
    Since Supabase stores the session in the client, we need to 
    synchronize it with Django's internal User object.
    """
    # Note: On the backend, we usually get a code/error or just the session
    # For a purely backend flow, we'd exchange a code here.
    # If the user is already signed in on Supabase's side, we fetch the email.
    
    res = supabase.auth.get_user()
    if res and res.user:
        email = res.user.email
        # Find or create a Django user with this email
        username = email.split('@')[0]
        user, created = User.objects.get_or_create(email=email, defaults={'username': username})
        
        # Log the user into Django
        login(request, user)
        messages.success(request, f"Successfully logged in via {res.user.app_metadata.get('provider', 'Social')}")
        return redirect('core:home')
        
    messages.error(request, "Failed to authenticate with social account.")
    return redirect('accounts:login')
