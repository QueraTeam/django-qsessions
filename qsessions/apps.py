from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoQsessionsConfig(AppConfig):
    name = "qsessions"
    verbose_name = _("Sessions")
