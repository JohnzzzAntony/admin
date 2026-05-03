import re
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

_COMMENT_RE = re.compile(r'<!--(?!\s*\[)[\s\S]*?-->')
_MULTI_SPACE_RE = re.compile(r'[ \t]+')
_LEADING_TRAILING_RE = re.compile(r'^[ \t]+|[ \t]+$', re.MULTILINE)
_MULTI_NEWLINE_RE = re.compile(r'\n+')


class StripHTMLCommentsMiddleware(MiddlewareMixin):
    """
    Strips HTML comments from outgoing responses and optionally minifies
    whitespace in production.

    Optimisations vs. naïve version:
      - Compiled regexes (module-level singletons, not recompiled each call).
      - Early-exits: skips non-HTML responses and streaming responses.
      - Only re-encodes the response when the content actually changed.
    """

    def process_response(self, request, response):
        # Skip non-HTML and streaming responses (no .content attribute)
        content_type = response.get('Content-Type', '')
        if 'text/html' not in content_type or getattr(response, 'streaming', False):
            return response

        content = response.content.decode('utf-8', errors='ignore')

        # Strip HTML comments (preserve IE conditional comments: <!--[if …]>)
        new_content = _COMMENT_RE.sub('', content)

        if not settings.DEBUG:
            # Basic whitespace minification in production only
            new_content = _MULTI_SPACE_RE.sub(' ', new_content)
            new_content = _LEADING_TRAILING_RE.sub('', new_content)
            new_content = _MULTI_NEWLINE_RE.sub('\n', new_content)

        # Avoid re-encoding if nothing changed (saves ~1 alloc per request)
        if new_content is not content and new_content != content:
            response.content = new_content.encode('utf-8')

        return response

