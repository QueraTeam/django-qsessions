from datetime import datetime, timedelta

import pytest
from django.core.management import call_command

from qsessions.models import Session


@pytest.mark.django_db
def test_can_call():
    Session.objects.create(
        session_key="s1",
        expire_date=datetime.now() + timedelta(hours=1),
        ip="127.0.0.1",
    )
    Session.objects.create(
        session_key="s2",
        expire_date=datetime.now() - timedelta(hours=1),
        ip="127.0.0.1",
    )
    assert Session.objects.count() == 2
    call_command("clearsessions")
    assert Session.objects.count() == 1
