from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^config/$', views.admin),
    url(r'^vote/$', views.vote),
    url(r'^$', RedirectView.as_view(url='/vote/')),
    url(r'^', views.http404)
]
