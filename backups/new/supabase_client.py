"""
core/supabase_client.py  ← REPLACE your existing file
=======================================================
Robust Supabase client singleton.
Reads SUPABASE_URL and SUPABASE_KEY from environment / .env.
Returns None gracefully if credentials are missing so the rest of the
app can still function without crashing.
"""

import os
import logging

logger = logging.getLogger(__name__)

_supabase_client = None   # module-level singleton


def get_supabase():
    """
    Return a configured Supabase client, or None if credentials are absent.
    Uses a module-level singleton so the client is only created once.
    """
    global _supabase_client

    if _supabase_client is not None:
        return _supabase_client

    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()

    if not url or not key:
        logger.warning(
            "Supabase credentials missing (SUPABASE_URL / SUPABASE_KEY). "
            "Social auth will be unavailable."
        )
        return None

    try:
        from supabase import create_client
        _supabase_client = create_client(url, key)
        logger.info("Supabase client initialised successfully.")
        return _supabase_client
    except Exception as exc:
        logger.error("Failed to initialise Supabase client: %s", exc)
        return None


# Convenience singleton — import this anywhere with:
#   from core.supabase_client import supabase
supabase = get_supabase()
