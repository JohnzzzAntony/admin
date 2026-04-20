# JKR — Supabase Auth + Email Notifications Setup Guide
# =======================================================

## Files in this package

| File | What to do |
|------|-----------|
| `core/supabase_client.py`               | REPLACE existing file |
| `accounts/views.py`                     | REPLACE existing file |
| `accounts/urls.py`                      | REPLACE existing file |
| `accounts/signals.py`                   | REPLACE existing file |
| `accounts/email_notifications.py`       | NEW — create this file |
| `orders/notifications.py`               | REPLACE existing file |
| `templates/accounts/oauth_callback.html`| NEW — create this file |
| `templates/accounts/social_buttons_snippet.html` | NEW — paste into login.html & register.html |
| `settings_additions.py`                 | ADD contents to jkr/settings.py |
| `env_additions.txt`                     | ADD contents to .env / .env.local |

Google OAuth files from any previous setup — DELETE them:
  ✕ accounts/google_oauth.py   (delete this file if it exists)

---

## Step 1 — Supabase Dashboard Setup

### 1a. Get your API credentials
1. Go to https://supabase.com and open your project
2. Settings → API
3. Copy "Project URL" → this is your SUPABASE_URL
4. Copy "anon public" key → this is your SUPABASE_KEY

### 1b. Enable social providers
1. Authentication → Providers
2. Enable the ones you want — the most common are:
   - Google (requires Google Cloud Console Client ID + Secret)
   - GitHub (requires GitHub OAuth App Client ID + Secret)
   - Facebook, Discord, Apple, etc.

For Google specifically:
   a. Go to https://console.cloud.google.com
   b. APIs & Services → Credentials → Create OAuth 2.0 Client ID (Web application)
   c. Authorised redirect URIs — add BOTH:
        https://your-project-ref.supabase.co/auth/v1/callback   ← Supabase handles OAuth
        http://localhost:8000/accounts/callback/                  ← local dev
        https://yourdomain.com/accounts/callback/                 ← production
   d. Paste Client ID + Secret into Supabase → Authentication → Providers → Google

### 1c. Set your callback URL in Supabase
1. Authentication → URL Configuration
2. Site URL: https://yourdomain.com  (or http://localhost:8000 for dev)
3. Redirect URLs — add:
     http://localhost:8000/accounts/callback/
     https://yourdomain.com/accounts/callback/

---

## Step 2 — Install dependencies

    pip install supabase

(The supabase Python package is likely already installed in your project.)

---

## Step 3 — Environment variables

Add the lines from env_additions.txt to your .env.local (development) or .env (production).

---

## Step 4 — Settings

Paste the contents of settings_additions.py at the end of the EMAIL section in jkr/settings.py.

---

## Step 5 — Copy files

Copy each file to its matching location in your project (see table above).

---

## Step 6 — Add social buttons to your templates

In templates/accounts/login.html — paste this inside your form, below the submit button:

    {% include "accounts/social_buttons_snippet.html" %}

Do the same in templates/accounts/register.html.

---

## Step 7 — Delete old Google OAuth file (if it exists)

    rm accounts/google_oauth.py

---

## How it all works

### Social login flow (e.g. user clicks "Continue with Google")
1. /accounts/social/google/ → social_login view → Supabase generates Google consent URL
2. User approves on Google → Supabase redirects to /accounts/callback/#access_token=xxx
3. oauth_callback.html (JS) extracts token from URL hash → POSTs it to /accounts/callback/
4. social_callback view → verifies token with Supabase → creates/finds Django User → login()
5. send_welcome_email() fires for brand-new accounts
6. User lands on core:home ✓

### Email notifications
| Event | Triggered by | Email sent |
|-------|-------------|-----------|
| New registration (form) | register_view | Welcome email |
| New registration (OAuth) | social_callback | Welcome email |
| Any login | user_logged_in signal | Login alert |
| New order | CustomerOrder.save() | Order confirmation |
| Order status change | CustomerOrder.save() | Status update |
| Payment confirmed | Call manually in webhook view | Payment confirmation |

### Manually triggering payment confirmation email (in your Stripe/Tabby webhook view):
    from orders.notifications import send_customer_notification
    send_customer_notification(order, notification_type='payment_confirmation')

### Toggle email notifications
In Django Admin → Site Settings → enable_email_notifications (on/off switch).

### Test emails without sending
Add to .env.local:
    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
This prints all emails to your terminal. Switch back to smtp for real sends.
