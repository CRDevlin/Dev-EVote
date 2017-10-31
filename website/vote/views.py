from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from .models import Record
from .forms import *


def http404(request):
    return HttpResponseNotFound(render(request, "404.html"))


def http500(request):
    return HttpResponseNotFound(render(request, "500.html"))


def admin(request):
    return render(request, "admin.html")


def index(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)

        if form.is_valid():
            token = form.cleaned_data['token']
            # tue = Record.objects.get(token=token)
            return HttpResponse(token)
    else:
        form = TokenForm()

    return render(request, "index.html", {'form': form})


def vote(request):
    if request.method == 'POST':
        form = VoteForm(request.POST)

        if form.is_valid():
            choice = form.cleaned_data['choice']
            return HttpResponse(choice)
    else:
        form = VoteForm()

    return render(request, "vote.html", {'form': form})


def new_election(request):
    if request.method == 'POST':
        form = ElectionUploadForm(request.POST)

        if form.is_valid():
            return HttpResponse("Uploaded")
    else:
        form = ElectionUploadForm()

    return render(request, "new_election.html", {'form': form})
