from importlib import import_module
from django.conf import settings

def get_session_store_class(*_):
    engine = import_module(settings.SESSION_ENGINE)
    return engine.SessionStore
