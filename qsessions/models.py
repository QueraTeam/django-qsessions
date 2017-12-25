from django.contrib.sessions.base_session import AbstractBaseSession, BaseSessionManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from importlib import import_module


class SessionManager(BaseSessionManager):
    use_in_migrations = True


class Session(AbstractBaseSession):
    """
    Session objects containing user session information.
    """
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
                             null=True, on_delete=models.CASCADE)
    user_agent = models.CharField(null=True, blank=True, max_length=300)
    # created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_('IP'))

    objects = SessionManager()

    @classmethod
    def get_session_store_class(cls):
        from qsessions.backends.cached_db import SessionStore
        return SessionStore

    def delete(self, *args, **kwargs):
        """
        Delete session from both DB and cache (first DB, then cache)
        """
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        session = SessionStore(session_key=self.session_key)
        r = super(Session, self).delete(*args, **kwargs)
        session.delete()
        return r
