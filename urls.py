from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<role_id>[0-9]+)/accessResults/$', views.accessResults, name='accessResults'),
]
