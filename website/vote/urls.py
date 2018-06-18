from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^new_election/$', views.new_election, name='new_election'),
    url(r'^new_election$', RedirectView.as_view(url='new_election/')),
    url(r'^result/$', views.results, name='result'),
    url(r'^result$', RedirectView.as_view(url='result/')),
    url(r'^admin/$', views.admin),
    url(r'^admin$', RedirectView.as_view(url='admin/')),
    url(r'^vote/$', views.vote),
    url(r'^vote$', RedirectView.as_view(url='vote/')),
    url(r'^recover/$', views.voter_token_recover, name='recover'),
    url(r'^recover$', RedirectView.as_view(url='recover/')),
    url(r'^$', views.index),
    url(r'^', views.http404)
]
