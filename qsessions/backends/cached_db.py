from django.contrib.sessions.backends.cached_db import SessionStore as CachedDBStore
from .common import QSessionStoreMixin

KEY_PREFIX = "qsessions.q_cached_db"


class SessionStore(QSessionStoreMixin, CachedDBStore):
    """
    Implements cached, database backed sessions, with a foreign key to User.
    It also stores IP and User Agent.
    """
    cache_key_prefix = KEY_PREFIX
