from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.urls import path


def read_session(request):
    return JsonResponse(dict(request.session))


def modify_session(request):
    request.session["FOO"] = "BAR"
    return HttpResponse("")


urlpatterns = [
    path("read_session/", read_session),
    path("modify_session/", modify_session),
    path("admin/", admin.site.urls),
]
