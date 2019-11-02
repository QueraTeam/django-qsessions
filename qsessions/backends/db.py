from django.contrib.sessions.backends.db import SessionStore as DBStore
from .common import QSessionStoreMixin


class SessionStore(QSessionStoreMixin, DBStore):
    """
    Implements database backed sessions, with a foreign key to User.
    It also stores IP and User Agent.
    """
    pass
