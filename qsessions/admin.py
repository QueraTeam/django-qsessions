from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.utils.timezone import now
from django.contrib import admin
from django.urls import reverse
from .models import Session
from pprint import pformat


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
    readonly_fields = (
        "ip",
        "location",
        "user",
        "user_agent",
        "is_valid",
        "expire_date",
        "created_at",
        "updated_at",
        "user_agent",
        "device",
        "session_key",
        "session_data_decoded",
    )
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
            "user__%s" % getattr(User, "USERNAME_FIELD", "username"),
            "user__%s" % getattr(User, "USERNAME_EMAIL", "email"),
        )

    def is_valid(self, obj):
        return obj.expire_date > now()

    is_valid.boolean = True
    is_valid.short_description = _("Is valid")

    def session_data_decoded(self, obj):
        return format_html(
            '<pre style="white-space: pre-wrap; max-width: 800px; display: inline-block; direction: ltr;">{}</pre>',
            pformat(obj.get_decoded()),
        )

    session_data_decoded.short_description = _("Session data")
