from django.core.management import call_command


def test_system_checks():
    call_command("check")
