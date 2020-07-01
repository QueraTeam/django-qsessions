# -- encoding: UTF-8 --
from __future__ import unicode_literals

import pytest
from django.conf import settings


@pytest.mark.django_db
def test_smoke_admin(admin_client):
    admin_client.get("/modify_session/", HTTP_USER_AGENT="Chrome/70.0.3538.102", REMOTE_ADDR="89.160.20.112")
    resp = admin_client.get("/admin/qsessions/session/?active=1&owner=my")
    assert resp.status_code == 200
    content = resp.content.decode("UTF-8")
    assert "Linköping, Sweden" in content  # From REMOTE_ADDR
    assert "Chrome 70.0.3538" in content  # From HTTP_USER_AGENT
    resp = admin_client.get(
        "/admin/qsessions/session/%s/change/" % admin_client.cookies[settings.SESSION_COOKIE_NAME].value
    )
    assert "FOO" in resp.content.decode("UTF-8")  # Set by modify_session
