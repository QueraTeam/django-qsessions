from functools import cached_property
from importlib import import_module

from django.conf import settings
from django.contrib.sessions.base_session import AbstractBaseSession, BaseSessionManager
from django.core.cache import caches
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import qsessions.geoip as geoip


class SessionQuerySet(models.QuerySet):
    def delete(self):
        """
        Delete sessions from both DB and cache (first cache, then DB)
        """
        # noinspection PyPep8Naming
        SessionStore = Session.get_session_store_class()
        prefix = getattr(SessionStore, "cache_key_prefix", None)
        if prefix is not None:
            caches[settings.SESSION_CACHE_ALIAS].delete_many(prefix + s.session_key for s in self)
        return super().delete()


class SessionManager(BaseSessionManager.from_queryset(SessionQuerySet)):
    use_in_migrations = True


class Session(AbstractBaseSession):
    """
    Session objects containing user session information.
    """

    user = models.ForeignKey(getattr(settings, "AUTH_USER_MODEL", "auth.User"), null=True, on_delete=models.CASCADE)
    user_agent = models.CharField(null=True, blank=True, max_length=300)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_("IP"))

    objects = SessionManager()

    @classmethod
    def get_session_store_class(cls):
        return import_module(settings.SESSION_ENGINE).SessionStore

    def save(self, *args, **kwargs):
        # FIXME: find a better solution for `created_at` field which does not need an extra query.
        # https://code.djangoproject.com/ticket/17654
        try:
            self.created_at = Session.objects.get(pk=self.pk).created_at
        except Session.DoesNotExist:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Delete session from both DB and cache (first cache, then DB)
        """
        # noinspection PyPep8Naming
        SessionStore = Session.get_session_store_class()
        prefix = getattr(SessionStore, "cache_key_prefix", None)
        if prefix is not None:
            caches[settings.SESSION_CACHE_ALIAS].delete(prefix + self.session_key)
        return super().delete(*args, **kwargs)

    @cached_property
    def location_info(self) -> dict:
        return geoip.ip_to_location_info(self.ip)

    @cached_property
    def location(self) -> str:
        return geoip.ip_to_location(self.ip)

    @cached_property
    def device_info(self):
        """
        Describe the user agent of this session, if any
        :rtype: ua_parser.core.Result | None
        """
        if self.user_agent:
            from ua_parser import parse  # late import to avoid import cost

            return parse(self.user_agent)
        return None

    @cached_property
    def device(self) -> str:
        if device := self.device_info:

            def get_version_string(version_info):
                try:
                    return ".".join(version_info[: version_info.index(None)])
                except ValueError:
                    return ".".join(version_info)

            return "{device} / {os} / {browser}".format(
                device=device.device.family if device.device else "Other",
                os=(
                    f"{device.os.family} {get_version_string([device.os.major, device.os.minor, device.os.patch, device.os.patch_minor])}"
                    if device.os
                    else "Other"
                ),
                browser=(
                    f"{device.user_agent.family} {get_version_string([device.user_agent.major, device.user_agent.minor, device.user_agent.patch, device.user_agent.patch_minor])}"
                    if device.user_agent
                    else "Other"
                ),
            )
        return ""
