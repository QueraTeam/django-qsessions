from django.contrib.sessions.backends.cached_db import SessionStore as CachedDBStore
from qsessions import IP_SESSION_KEY, USER_AGENT_SESSION_KEY
from django.contrib import auth

KEY_PREFIX = "qsessions.q_cached_db"


class SessionStore(CachedDBStore):
    """
    Implements cached, database backed sessions, with a foreign key to User.
    It also stores IP and User Agent.
    """
    cache_key_prefix = KEY_PREFIX

    def __init__(self, session_key=None, user_agent=None, ip=None):
        self.modified = False
        self.user_agent = user_agent[:300] if user_agent else user_agent
        self.ip = ip
        super(SessionStore, self).__init__(session_key)

    @classmethod
    def get_model_class(cls):
        from qsessions.models import Session
        return Session

    def load(self):
        data = super(SessionStore, self).load()
        if data.get(USER_AGENT_SESSION_KEY) != self.user_agent \
                or data.get(IP_SESSION_KEY) != self.ip:
            # If IP or User Agent has changed, set modified to True in order to save
            # the new IP and User Agent in both Cache and DB
            self.modified = True
        return data

    def save(self, must_create=False):
        # Store IP and User Agent in session_data
        if USER_AGENT_SESSION_KEY not in self or self[USER_AGENT_SESSION_KEY] != self.user_agent:
            self[USER_AGENT_SESSION_KEY] = self.user_agent
        if IP_SESSION_KEY not in self or self[IP_SESSION_KEY] != self.ip:
            self[IP_SESSION_KEY] = self.ip
        super(SessionStore, self).save(must_create)

    def create_model_instance(self, data):
        # Store User, User Agent, and IP in Session (in DB).
        return self.model(
            session_key=self._get_or_create_session_key(),
            session_data=self.encode(data),
            expire_date=self.get_expiry_date(),
            user_id=self.get(auth.SESSION_KEY),
            user_agent=self.user_agent,
            ip=self.ip
        )
