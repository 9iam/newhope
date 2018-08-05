from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.hello),
    url('^(?P<id>\d+)$', views.hello),
    url('^cat$', views.poem),
]
