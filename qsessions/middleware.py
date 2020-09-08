from django.contrib.sessions.middleware import SessionMiddleware as DjSessionMiddleware
from django.conf import settings
from ipware import get_client_ip


class SessionMiddleware(DjSessionMiddleware):
    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        request.session = self.SessionStore(
            ip=get_client_ip(request)[0],
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            session_key=session_key,
        )
