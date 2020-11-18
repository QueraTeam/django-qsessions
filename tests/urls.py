from django.contrib import admin
from django.http import HttpResponse, JsonResponse

try:
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import url


def read_session(request):
    return JsonResponse(dict(request.session))


def modify_session(request):
    request.session["FOO"] = "BAR"
    return HttpResponse("")


urlpatterns = [
    url(r"^read_session/$", read_session),
    url(r"^modify_session/$", modify_session),
    url(r"^admin/", admin.site.urls),
]
