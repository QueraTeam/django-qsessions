import json

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse

from qsessions import USER_AGENT_SESSION_KEY
from qsessions.models import Session


@pytest.mark.django_db
def test_unmodified_session(client):
    client.get('/', HTTP_USER_AGENT='TestUA/1.1')
    assert settings.SESSION_COOKIE_NAME not in client.cookies


@pytest.mark.django_db
def test_modify_session(client):
    client.get('/read_session/', HTTP_USER_AGENT='TestUA/1.1')
    client.get('/modify_session/', HTTP_USER_AGENT='TestUA/1.1')
    data = json.loads(client.get('/read_session/', HTTP_USER_AGENT='TestUA/1.1').content.decode('UTF-8'))
    assert data['FOO'] == 'BAR'
    assert data[USER_AGENT_SESSION_KEY] == 'TestUA/1.1'

    assert settings.SESSION_COOKIE_NAME in client.cookies
    session = Session.objects.get(
        pk=client.cookies[settings.SESSION_COOKIE_NAME].value
    )
    assert session.user_agent == 'TestUA/1.1'
    assert session.ip == '127.0.0.1'


@pytest.mark.django_db
def test_login(client):
    admin_login_url = reverse('admin:login')
    user = User.objects.create_superuser('bouke', '', 'secret')
    response = client.post(admin_login_url,
        data={
            'username': 'bouke',
            'password': 'secret',
            'this_is_the_login_form': '1',
            'next': '/admin/'
        },
        HTTP_USER_AGENT='TestUA/1.1',

    )
    assert response.url == '/admin/'
    session = Session.objects.get(
        pk=client.cookies[settings.SESSION_COOKIE_NAME].value
    )
    assert user == session.user


@pytest.mark.django_db
def test_long_ua(client):
    client.get('/modify_session/', HTTP_USER_AGENT=''.join('a' for _ in range(500)))
