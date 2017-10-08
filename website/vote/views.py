from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template import RequestContext, loader


def http404(request):
    return HttpResponseNotFound(render(request, "404.html"))


def http500(request):
    return HttpResponseNotFound(render(request, "500.html"))


def admin(request):
    return render(request, "admin.html")


def vote(request):
    return render(request, "vote.html")

