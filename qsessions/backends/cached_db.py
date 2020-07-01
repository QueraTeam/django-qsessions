from django.contrib.sessions.backends.cached_db import SessionStore as DjangoCachedDBStore

from .db import SessionStore as QSessionsDBStore

KEY_PREFIX = "qsessions.q_cached_db"


class SessionStore(QSessionsDBStore, DjangoCachedDBStore):
    """
    Implements cached, database backed sessions, with a foreign key to User.
    It also stores IP and User Agent.
    """

    cache_key_prefix = KEY_PREFIX
