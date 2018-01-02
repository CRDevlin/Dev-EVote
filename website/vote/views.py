import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

from .forms import *
from .handlers import handle_uploaded_file
from .transaction import *
from website.settings import CONFIG


def admin(request):
    return render(request, "admin.html")


def http404(request):
    return HttpResponseNotFound(render(request, "404.html"))


def http500(request):
    return HttpResponseNotFound(render(request, "500.html"))


def index(request):
    if request.method == 'POST':
        form = VoteTokenForm(CONFIG['VOTE_TOKEN_LEN'], request.POST)

        if form.is_valid():
            token = form.cleaned_data['token']

            try:
                validate_voter_token(token)
                request.session['valid_token'] = token
                return HttpResponseRedirect("/vote/")
            except LookupError as e:
                print(e)
            except ValueError as e:
                print(e)
    else:
        form = VoteTokenForm(CONFIG['VOTE_TOKEN_LEN'])

    return render(request, "token_form.html", {'form': form})


def new_election(request):
    if request.method == 'POST':
        form = ElectionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(CONFIG['VOTER_PATH'], form.cleaned_data['voter_file'])
            handle_uploaded_file(CONFIG['NOMINEE_PATH'], form.cleaned_data['nominee_file'])
            result = create_election(CONFIG['VOTER_PATH'],
                                     CONFIG['NOMINEE_PATH'],
                                     form.cleaned_data["anonymous"],
                                     form.cleaned_data["multi_vote"],
                                     form.cleaned_data["date"],
                                     form.cleaned_data["time"])
            return HttpResponse("Election created. The election token is <b>" + result + "</b>")
        else:
            print(form.errors)
    else:
        form = ElectionUploadForm()

    return render(request, "new_election.html", {'form': form})


def results(request):
    if request.method == 'POST':
        form = ElectionResTokenForm(CONFIG['ELEC_TOKEN_LEN'], request.POST)

        if form.is_valid():
            token = form.cleaned_data['token']
            try:
                validate_election_token(token)
                res = get_election_results(token)
                return render(request, "results.html", {'ballot': res['BALLOT'], 'result': res['RESULT'], 'winner': res['WINNER']})
            except LookupError as e:
                print(e)
            except ValueError as e:
                print(e)
    else:
        form = ElectionResTokenForm(CONFIG['ELEC_TOKEN_LEN'])

    return render(request, "token_form.html", {'form': form})


def vote(request):
    if 'valid_token' not in request.session:
        return HttpResponseRedirect("/")

    token = request.session['valid_token']

    choices = get_nominee_choices(token)

    if request.method == 'POST':
        form = VoteForm(choices, request.POST)

        if form.is_valid():
            choice = int(form.cleaned_data['choice'])
            set_nominee_choice(token, choice)
            request.session.flush()
            return HttpResponseRedirect("/")
    else:
        form = VoteForm(choices)

    return render(request, "vote.html", {'form': form})
