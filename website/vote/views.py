import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from .forms import *
from .handlers import handle_uploaded_file
from .transaction import *

max_chunk_size = 1024
voter_path = 'uploaded/voter.json'
nominee_path = 'uploaded/nominee.json'


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

            return vote(token)
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
        form = ElectionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(voter_path, form.cleaned_data['voter_file'])
            handle_uploaded_file(nominee_path, form.cleaned_data['nominee_file'])
            create_election(voter_path,
                            nominee_path,
                            form.cleaned_data["anonymous"],
                            form.cleaned_data["multi_vote"],
                            form.cleaned_data["date"],
                            form.cleaned_data["time"])

            return HttpResponse("Uploaded")
        else:
            print(form.errors)
    else:
        form = ElectionUploadForm()

    return render(request, "new_election.html", {'form': form})
