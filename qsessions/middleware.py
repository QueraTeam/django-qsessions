from django.contrib.sessions.middleware import SessionMiddleware as DjSessionMiddleware
from django.conf import settings
from ipware.ip import get_real_ip, get_ip


class SessionMiddleware(DjSessionMiddleware):

    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        request.session = self.SessionStore(
            ip=get_real_ip(request) or get_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            session_key=session_key
        )
