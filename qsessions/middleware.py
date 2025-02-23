from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware as DjSessionMiddleware


class SessionMiddleware(DjSessionMiddleware):
    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        request.session = self.SessionStore(
            ip=request.META.get("REMOTE_ADDR", None),
            user_agent=request.headers.get("User-Agent", ""),
            session_key=session_key,
        )
