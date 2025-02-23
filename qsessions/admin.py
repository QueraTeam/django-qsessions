from pprint import pformat

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .models import Session


def linkify(field_name):
    """
    Converts a foreign key value into clickable links.
    """

    def _linkify(obj):
        linked_obj = getattr(obj, field_name)
        if linked_obj is None:
            return "-"
        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f"admin:{app_label}_{model_name}_change"
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = field_name  # Sets column name
    return _linkify


class ExpiredFilter(admin.SimpleListFilter):
    title = _("Is Valid")
    parameter_name = "active"

    def lookups(self, request, model_admin):
        return [("1", _("Active")), ("0", _("Expired"))]

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(expire_date__gt=now())
        elif self.value() == "0":
            return queryset.filter(expire_date__lte=now())


class OwnerFilter(admin.SimpleListFilter):
    title = _("Owner")
    parameter_name = "owner"

    def lookups(self, request, model_admin):
        return [("my", _("Self"))]

    def queryset(self, request, queryset):
        if self.value() == "my":
            return queryset.filter(user=request.user)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("ip", linkify("user"), "is_valid", "created_at", "expire_date", "device", "location")
    list_select_related = ("user",)
    list_filter = ExpiredFilter, OwnerFilter
    fields = (
        "user",
        "ip",
        "location",
        "is_valid",
        "created_at",
        "updated_at",
        "expire_date",
        "user_agent",
        "device",
        "session_key",
        "session_data_decoded",
    )
    ordering = ("-expire_date",)

    def get_search_fields(self, request):
        # noinspection PyPep8Naming
        User = get_user_model()
        return (
            "ip",
            f"user__{getattr(User, 'USERNAME_FIELD', 'username')}",
            f"user__{getattr(User, 'USERNAME_EMAIL', 'email')}",
        )

    @admin.display(description=_("Is valid"), boolean=True)
    def is_valid(self, obj: Session):
        return obj.expire_date > now()

    @admin.display(description=_("Session data"))
    def session_data_decoded(self, obj: Session):
        return format_html(
            '<pre style="white-space: pre-wrap; max-width: 800px; display: inline-block; direction: ltr;">{}</pre>',
            pformat(obj.get_decoded()),
        )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
