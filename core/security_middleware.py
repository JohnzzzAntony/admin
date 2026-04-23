import logging
from django.http import HttpResponseForbidden
from django.conf import settings

logger = logging.getLogger(__name__)

class SecurityShieldMiddleware:
    """
    Blocks known malicious user agents, scanners, and common vulnerability probes.
    """
    
    BAD_USER_AGENTS = [
        "sqlmap", "nikto", "dirbuster", "dirb", "netsparker", "nessus", 
        "nmap", "acunetix", "w3af", "harvest", "grabber", "censys", "zgrab"
    ]
    
    BLOCK_PATHS = [
        ".env", ".git", ".php", "wp-admin", "wp-login", "xmlrpc.php",
        "config.php", "database.sql", "dump.sql", ".htaccess", "id_rsa"
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        path = request.path.lower()

        # 1. Block malicious user agents
        if any(ua in user_agent for ua in self.BAD_USER_AGENTS):
            logger.warning(f"Blocked malicious User-Agent: {user_agent} at {request.path}")
            return HttpResponseForbidden("Security Shield: Access Denied.")

        # 2. Block sensitive path probes (common in bot scans)
        if any(path.endswith(p) or f"/{p}/" in path for p in self.BLOCK_PATHS):
            logger.warning(f"Blocked probe for sensitive path: {request.path} from IP: {request.META.get('REMOTE_ADDR')}")
            return HttpResponseForbidden("Security Shield: Prohibited Access.")

        return self.get_response(request)
