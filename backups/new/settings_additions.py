# ================================================================
# jkr/settings.py  — ADD this block to your existing settings file
# ================================================================
# Paste it after the EMAIL section (around line 220).
# ================================================================

# =============================================================================
# SUPABASE AUTH
# =============================================================================
# 1. Go to https://supabase.com → your project → Settings → API
# 2. Copy "Project URL" → SUPABASE_URL
# 3. Copy "anon public" key → SUPABASE_KEY
# 4. Go to Authentication → Providers and enable the ones you want
#    (Google, GitHub, Facebook, Discord, etc.)
# 5. Go to Authentication → URL Configuration and add your callback URL:
#      Development : http://localhost:8000/accounts/callback/
#      Production  : https://yourdomain.com/accounts/callback/

SUPABASE_URL = env("SUPABASE_URL", default="")
SUPABASE_KEY = env("SUPABASE_KEY", default="")
