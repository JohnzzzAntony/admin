from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Your account has been created.")
            return redirect('core:home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()
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
from django.contrib.auth.models import User
from django.conf import settings

def social_login(request, provider):
    """
    Initiate a social login via Supabase.
    Redirects user to the social provider's login page.
    """
    try:
        from core.supabase_client import supabase
        if not supabase:
            messages.error(request, "Social login is not available right now. Please use email login.")
            return redirect('accounts:login')

        # Build the full callback URL for your local or live site
        redirect_to = request.build_absolute_uri('/accounts/callback/')

        # Generate the OAuth login URL
        result = supabase.auth.sign_in_with_oauth({
            "provider": provider,
            "options": {"redirect_to": redirect_to}
        })

        if hasattr(result, 'url') and result.url:
            return redirect(result.url)

        messages.error(request, "Could not initiate social login. Please try again.")
        return redirect('accounts:login')

    except Exception as e:
        messages.error(request, "Social login is currently unavailable. Please use email login.")
        return redirect('accounts:login')

def social_callback(request):
    """
    Handles the return logic from Supabase OAuth.
    Synchronizes Supabase user with Django's internal User object.
    """
    try:
        from core.supabase_client import supabase
        if not supabase:
            messages.error(request, "Authentication failed. Please use email login.")
            return redirect('accounts:login')

        res = supabase.auth.get_user()
        if res and res.user:
            email = res.user.email
            if not email:
                raise ValueError("No email returned from social provider.")

            username = email.split('@')[0]
            # get_or_create with email as unique key
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'username': username, 'first_name': username}
            )

            if not created and user.username != username:
                pass  # Existing user, keep their username

            login(request, user)
            provider = res.user.app_metadata.get('provider', 'Social') if res.user.app_metadata else 'Social'
            messages.success(request, f"Successfully logged in via {provider.capitalize()}!")
            return redirect('core:home')

        messages.error(request, "Failed to authenticate. Please try again.")
        return redirect('accounts:login')

    except Exception as e:
        messages.error(request, "Authentication failed. Please use email & password login.")
        return redirect('accounts:login')
