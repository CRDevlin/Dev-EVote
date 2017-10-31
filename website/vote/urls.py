from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^new_election/$', views.new_election),
    url(r'^new_election$', RedirectView.as_view(url='new_election/')),
    url(r'^config/$', views.admin),
    url(r'^config$', RedirectView.as_view(url='config/')),
    url(r'^vote/$', views.vote),
    url(r'^vote$', RedirectView.as_view(url='vote/')),
    url(r'^$', views.index),
    url(r'^', views.http404)
]
