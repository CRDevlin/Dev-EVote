from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template import RequestContext, loader

from .models import Record

def http404(request):
    return HttpResponseNotFound(render(request, "404.html"))


def http500(request):
    return HttpResponseNotFound(render(request, "500.html"))


def admin(request):
    return render(request, "admin.html")


def vote(request):
    # If form has posted
    if request.POST:
        if 'token' in request.POST:
            token = request.POST.get('token', '')
            record = Record.objects.get(id=token)
            return HttpResponse("Record Obtained!")
    else:
        return render(request, "vote.html")
