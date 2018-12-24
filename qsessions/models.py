from django.conf import settings
from django.contrib.sessions.base_session import AbstractBaseSession, BaseSessionManager
from django.core.cache import caches
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

import qsessions.geoip as geoip
from qsessions.backends.cached_db import SessionStore


class SessionQuerySet(models.QuerySet):
    def delete(self):
        """
        Delete sessions from both DB and cache (first cache, then DB)
        """
        caches[settings.SESSION_CACHE_ALIAS].delete_many(SessionStore.cache_key_prefix + s.session_key for s in self)
        return super(SessionQuerySet, self).delete()


class SessionManager(BaseSessionManager.from_queryset(SessionQuerySet)):
    use_in_migrations = True


class Session(AbstractBaseSession):
    """
    Session objects containing user session information.
    """
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
                             null=True, on_delete=models.CASCADE)
    user_agent = models.CharField(null=True, blank=True, max_length=300)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_('IP'))

    objects = SessionManager()

    @classmethod
    def get_session_store_class(cls):
        return SessionStore

    def save(self, *args, **kwargs):
        # FIXME: find a better solution for `created_at` field which does not need an extra query.
        # https://code.djangoproject.com/ticket/17654
        try:
            self.created_at = Session.objects.get(pk=self.pk).created_at
        except Session.DoesNotExist:
            self.created_at = timezone.now()
        super(Session, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Delete session from both DB and cache (first cache, then DB)
        """
        caches[settings.SESSION_CACHE_ALIAS].delete(SessionStore.cache_key_prefix + self.session_key)
        return super(Session, self).delete(*args, **kwargs)

    def location(self):
        return geoip.ip_to_location(self.ip)

    def location_info(self):
        return geoip.ip_to_location_info(self.ip)

    def device(self):
        """
        Describe the user agent of this session, if any
        :rtype: user_agents.parsers.UserAgent | None
        """
        if self.user_agent:
            import user_agents  # late import to avoid import cost
            return user_agents.parse(self.user_agent)
        return None
