from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^config/$', views.admin),
    url(r'^vote/$', views.vote),
    # url(r'^config$', RedirectView.as_view(url='/admin/')),
    url(r'^$', RedirectView.as_view(url='/vote/')),
    url(r'^', views.http404),
    url(r'^submit_token$', 'TasksManager.views.submit_token.page', name="submit_token"),
]
