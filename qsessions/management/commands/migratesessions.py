from django.apps import apps
from django.conf import settings
from django.contrib.auth import SESSION_KEY, get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from qsessions.models import Session


class Command(BaseCommand):
    help = "Copy active sessions from Django's database session table to QSessions."

    def handle(self, *args, **options):
        if settings.SESSION_ENGINE not in (
            "django.contrib.sessions.backends.db",
            "django.contrib.sessions.backends.cached_db",
        ):
            raise CommandError(
                "Run migratesessions with Django's db or cached_db backend before changing SESSION_ENGINE."
            )
        if not apps.is_installed("django.contrib.sessions"):
            raise CommandError("Keep django.contrib.sessions in INSTALLED_APPS while migrating sessions.")

        source = apps.get_model("sessions", "Session")
        users = get_user_model()._base_manager
        copied = 0
        skipped_users = 0
        for row in source.objects.filter(expire_date__gt=timezone.now()).iterator():
            user_id = row.get_decoded().get(SESSION_KEY)
            if user_id is not None:
                try:
                    user_exists = users.filter(pk=user_id).exists()
                except (TypeError, ValueError, ValidationError):
                    user_exists = False
                if not user_exists:
                    skipped_users += 1
                    continue
            _, created = Session.objects.get_or_create(
                session_key=row.session_key,
                defaults={"session_data": row.session_data, "expire_date": row.expire_date, "user_id": user_id},
            )
            if created:
                copied += 1
        self.stdout.write(f"Copied {copied} sessions. Skipped {skipped_users} sessions with unknown users.")
