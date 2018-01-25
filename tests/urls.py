from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse


def empty(request):
    return HttpResponse('')


def modify_session(request):
    request.session['FOO'] = 'BAR'
    return HttpResponse('')


urlpatterns = [
    url(r'^$', empty),
    url(r'^modify_session/$', modify_session),
    url(r'^admin/', admin.site.urls),
]
