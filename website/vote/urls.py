from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /vote/
    # url(r'^vote/', views.vote, name='vote'),
    # ex:
    url(r'^$', views.vote, name='index'),
]
