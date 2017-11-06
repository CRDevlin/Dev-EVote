import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from .forms import *
from .queries import *
from .validation import validate_json, validate_content
from .handlers import handle_uploaded_file

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
        form = ElectionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(voter_path, request.FILES['voter_file'])
            handle_uploaded_file(nominee_path, request.FILES['nominee_file'])
            voters = json.load(open(voter_path))
            nominees = json.load(open(nominee_path))
            validate_json(voters,'voter')
            validate_json(nominees, 'nominee')
            validate_content(voters)
            validate_content(nominees)
            add_faculty(voters)
            add_faculty(nominees)

            return HttpResponse("Uploaded")
        else:
            print(form.errors)
    else:
        form = ElectionUploadForm()

    return render(request, "new_election.html", {'form': form})
