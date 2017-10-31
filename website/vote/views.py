from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template import RequestContext, loader

from .models import Record
from .forms import TokenForm

def http404(request):
    return HttpResponseNotFound(render(request, "404.html"))


def http500(request):
    return HttpResponseNotFound(render(request, "500.html"))


def admin(request):
    return render(request, "admin.html")


def vote(request):
    # If form has posted
    if request.method == 'POST':
        form = TokenForm(request.POST)

        if form.is_valid():
            token = form.cleaned_data['token']
            # tue = Record.objects.get(token=token)
            return HttpResponse("Record Obtained!")
    else:
        form = TokenForm()

    return render(request, "vote.html", {'form': form})

