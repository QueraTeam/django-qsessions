import pytest
from django.contrib import auth

from qsessions import IP_SESSION_KEY, USER_AGENT_SESSION_KEY
from qsessions.models import Session

SessionStore = Session.get_session_store_class()


@pytest.mark.django_db
def test_get_decoded(django_user_model):
    django_user_model.objects.create_user(username="test_user")

    store = SessionStore(user_agent="TestUA/1.1", ip="127.0.0.1")
    store[auth.SESSION_KEY] = 1
    store["foo"] = "bar"
    store.save()

    session = Session.objects.get(pk=store.session_key)
    assert session.get_decoded() == {
        "foo": "bar",
        auth.SESSION_KEY: 1,
        IP_SESSION_KEY: "127.0.0.1",
        USER_AGENT_SESSION_KEY: "TestUA/1.1",
    }


@pytest.mark.django_db
def test_very_long_ua():
    ua = (
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; ELT; "
        "BTRS29395; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ;  "
        "Embedded Web Browser from: http://bsalsa.com/; .NET CLR 2.0.50727; "
        ".NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; "
        ".NET CLR 1.1.4322; ELT; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; FDM; "
        ".NET4.0C; .NET4.0E; ELT)"
    )
    store = SessionStore(user_agent=ua, ip="127.0.0.1")
    store.save()

    session = Session.objects.get(pk=store.session_key)
    assert session.user_agent == ua[:300]


def test_location():
    session = Session(ip="89.160.20.112")
    assert session.location() == "Linköping, Sweden"
    loc_info = session.location_info()
    assert loc_info["city"] == "Linköping"
    assert loc_info["country_code"] == "SE"

    # This depends on Django version, so be safe
    assert loc_info.get("continent_code") == "EU" or loc_info.get("region") == "E"


def test_device():
    session = Session(
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/70.0.3538.102 Safari/537.36"
        )
    )
    device = session.device()
    assert device.os.family == "Mac OS X"
    assert device.browser.family == "Chrome"


@pytest.mark.django_db
def test_delete():
    """
    Session.delete should delete session from both DB and cache
    """
    store = SessionStore(user_agent="TestUA/1.1", ip="127.0.0.1")
    store.create()
    session_key = store.session_key

    session = Session.objects.get(pk=session_key)
    session.delete()

    assert not store.exists(session_key)


@pytest.mark.django_db
def test_bulk_delete_from_both_cache_and_db():
    s1 = SessionStore(user_agent="Python/2.7", ip="127.0.0.1")
    s1.create()
    s2 = SessionStore(user_agent="Python/2.7", ip="127.0.0.1")
    s2.create()
    s3 = SessionStore(user_agent="TestUA/1.1", ip="127.0.0.1")
    s3.create()
    assert s1.exists(s1.session_key)
    assert s2.exists(s2.session_key)
    assert s3.exists(s3.session_key)

    Session.objects.filter(user_agent="Python/2.7").delete()

    assert not s1.exists(s1.session_key)
    assert not s2.exists(s2.session_key)
    assert s3.exists(s3.session_key)
