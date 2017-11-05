import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from .models import Record
from .forms import *

max_chunk_size = 1024

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


def handle_uploaded_file(fileName, f):
    try:
        with open(fileName, 'wb+') as destination:
            if f.multiple_chunks():
                for chunk in f.chunks():
                    destination.write(chunk)
            else:
                destination.write(f.read())
    except:
        return False
    return True


def new_election(request):
    if request.method == 'POST':
        form = ElectionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            success = handle_uploaded_file('uploaded/voter.json', request.FILES['voter_file'])
            success = handle_uploaded_file('uploaded/nominee.json', request.FILES['nominee_file'])
            voters = json.load(open('uploaded/voter.json'))
            nominees = json.load(open('uploaded/nominee.json'))

            return HttpResponse("Uploaded")
        else:
            print(form.errors)
    else:
        form = ElectionUploadForm()

    return render(request, "new_election.html", {'form': form})
