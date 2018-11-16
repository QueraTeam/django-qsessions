from datetime import datetime, timedelta

import pytest
from django.core.management import call_command

from qsessions.models import Session


@pytest.mark.django_db
def test_can_call():
    Session.objects.create(
        expire_date=datetime.now() - timedelta(days=1),
        ip='127.0.0.1',
    )
    call_command('clearsessions')
    assert Session.objects.count() == 0
