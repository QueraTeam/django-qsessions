from datetime import timedelta

import pytest
from django.contrib import auth
from django.contrib.sessions.backends.base import CreateError
from django.conf import settings
from django.utils.timezone import now

from qsessions.models import Session
from qsessions.backends import get_session_store_class
SessionStore = get_session_store_class()
from qsessions.backends.cached_db import SessionStore as CachedBackend
from qsessions.backends.db import SessionStore as DBOnlyBackend

import time


@pytest.fixture(name='store')
def setup_store():
    return SessionStore(user_agent='TestUA/1.1', ip='127.0.0.1')


def test_untouched_init(store):
    assert store.modified is False
    assert store.accessed is False


def test_auth_session_key(store):
    assert auth.SESSION_KEY not in store
    assert store.modified is False
    assert store.accessed is True

    store.get(auth.SESSION_KEY)
    assert store.modified is False

    store[auth.SESSION_KEY] = 1
    assert store.modified is True


@pytest.mark.django_db
def test_save(store, django_user_model):
    django_user_model.objects.create_user(username='test_user')

    store[auth.SESSION_KEY] = 1
    store.save()

    session = Session.objects.get(pk=store.session_key)
    assert session.user_agent == 'TestUA/1.1'
    assert session.ip == '127.0.0.1'
    assert session.user_id == 1
    assert now() - timedelta(seconds=5) <= session.updated_at <= now()


@pytest.mark.django_db
def test_load_unmodified(store, django_user_model):
    django_user_model.objects.create_user(username='test_user')

    store[auth.SESSION_KEY] = 1
    store.save()
    store2 = SessionStore(session_key=store.session_key,
                          user_agent='TestUA/1.1', ip='127.0.0.1')
    store2.load()
    assert store2.user_agent == 'TestUA/1.1'
    assert store2.ip == '127.0.0.1'
    assert store2.get(auth.SESSION_KEY) == 1
    assert store2.modified is False


@pytest.mark.django_db
def test_load_modified(store, django_user_model):
    django_user_model.objects.create_user(username='test_user')

    store[auth.SESSION_KEY] = 1
    store.save()
    store2 = SessionStore(session_key=store.session_key,
                          user_agent='TestUA/1.1', ip='8.8.8.8')
    store2.load()
    assert store2.user_agent == 'TestUA/1.1'
    assert store2.ip == '8.8.8.8'
    assert store2.get(auth.SESSION_KEY) == 1
    assert store2.modified is True


@pytest.mark.django_db
def test_duplicate_create():
    s1 = SessionStore(session_key='DUPLICATE', user_agent='TestUA/1.1', ip='127.0.0.1')
    s1.create()
    s2 = SessionStore(session_key='DUPLICATE', user_agent='TestUA/1.1', ip='127.0.0.1')
    s2.create()
    assert s1.session_key != s2.session_key

    s3 = SessionStore(session_key=s1.session_key, user_agent='TestUA/1.1', ip='127.0.0.1')
    with pytest.raises(CreateError):
        s3.save(must_create=True)


@pytest.mark.django_db
def test_delete(store):
    # not persisted, should just return
    store.delete()

    # create, then delete
    store.create()
    session_key = store.session_key
    store.delete()

    # non-existing sessions, should not raise
    store.delete()
    store.delete(session_key)


@pytest.mark.django_db
def test_clear(store):
    """
    Clearing the session should clear all non-browser information
    """
    store[auth.SESSION_KEY] = 1
    store.clear()
    store.save()

    session = Session.objects.get(pk=store.session_key)
    assert session.user_id is None


def test_import():
    if settings.SESSION_ENGINE.endswith('.cached_db'):
        assert issubclass(SessionStore, CachedBackend)
    elif settings.SESSION_ENGINE.endswith('.db'):
        assert issubclass(SessionStore, DBOnlyBackend)
    else:
        assert False, "Unrecognised Session Engine"
