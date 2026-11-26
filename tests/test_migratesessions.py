from datetime import timedelta
from importlib import import_module

import pytest
from django.contrib.auth import BACKEND_SESSION_KEY, HASH_SESSION_KEY, SESSION_KEY, get_user
from django.contrib.sessions.backends.db import SessionStore as DjangoStore
from django.contrib.sessions.models import Session as DjangoSession
from django.core.management import CommandError, call_command
from django.test import RequestFactory
from django.utils import timezone

from qsessions.models import Session


@pytest.mark.django_db
@pytest.mark.parametrize(
    "source", ["django.contrib.sessions.backends.db", "django.contrib.sessions.backends.cached_db"]
)
def test_migrate_active_sessions(source, SessionStore, django_user_model, settings):
    source_store = import_module(source).SessionStore
    user = django_user_model.objects.create_user(username="member")
    authenticated = source_store()
    authenticated.update(
        {
            SESSION_KEY: str(user.pk),
            BACKEND_SESSION_KEY: "django.contrib.auth.backends.ModelBackend",
            HASH_SESSION_KEY: user.get_session_auth_hash(),
        }
    )
    authenticated.create()
    anonymous = source_store()
    anonymous["cart"] = ["milk"]
    anonymous.create()
    expired = source_store()
    expired.set_expiry(timezone.now() - timedelta(days=1))
    expired.create()
    source_row = DjangoSession.objects.get(pk=authenticated.session_key)

    settings.SESSION_ENGINE = source
    call_command("migratesessions")
    assert DjangoSession.objects.count() == 3
    assert Session.objects.count() == 2
    migrated = Session.objects.get(pk=authenticated.session_key)
    assert migrated.user == user
    assert migrated.session_data == source_row.session_data
    assert migrated.expire_date == source_row.expire_date
    assert migrated.ip is None and migrated.user_agent is None
    assert Session.objects.get(pk=anonymous.session_key).user is None

    settings.SESSION_ENGINE = SessionStore.__module__
    request = RequestFactory().get("/")
    request.session = SessionStore(authenticated.session_key)
    assert get_user(request) == user
    cart = SessionStore(anonymous.session_key)
    assert cart["cart"] == ["milk"]
    cart["cart"].append("eggs")
    cart.save()

    settings.SESSION_ENGINE = source
    call_command("migratesessions")
    assert Session.objects.count() == 2
    assert SessionStore(anonymous.session_key)["cart"] == ["milk", "eggs"]


@pytest.mark.django_db
def test_migrate_missing_user(django_user_model, settings):
    user = django_user_model.objects.create_user(username="deleted")
    original = DjangoStore()
    original[SESSION_KEY] = str(user.pk)
    original.create()
    user.delete()
    malformed = DjangoStore()
    malformed[SESSION_KEY] = "invalid-id"
    malformed.create()

    settings.SESSION_ENGINE = "django.contrib.sessions.backends.db"
    call_command("migratesessions")
    assert not Session.objects.exists()
    assert DjangoSession.objects.count() == 2


def test_migrate_after_switch():
    with pytest.raises(CommandError, match="before changing SESSION_ENGINE"):
        call_command("migratesessions")


def test_migrate_without_source_app(settings):
    settings.SESSION_ENGINE = "django.contrib.sessions.backends.db"
    settings.INSTALLED_APPS = [app for app in settings.INSTALLED_APPS if app != "django.contrib.sessions"]
    with pytest.raises(CommandError, match="INSTALLED_APPS"):
        call_command("migratesessions")
