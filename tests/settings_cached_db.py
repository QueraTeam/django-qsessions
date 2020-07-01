from .settings_base import *

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

SESSION_ENGINE = "qsessions.backends.cached_db"
