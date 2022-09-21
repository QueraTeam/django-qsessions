import pytest
from django.conf import settings

from qsessions.models import Session

SESSION_ENGINES = [
    "qsessions.backends.db",
    "qsessions.backends.cached_db",
]


@pytest.fixture(autouse=True, name="SessionStore", params=SESSION_ENGINES)
def session_store(request):
    settings.SESSION_ENGINE = request.param
    return Session.get_session_store_class()
