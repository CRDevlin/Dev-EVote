from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .forms import CommentForm


def index(request):
    return HttpResponse(CommentForm())


def detail(request, question_id):
    return HttpResponse("You're looking at question {}.".format(question_id))


def results(request, question_id):
    response = "You're looking at the results of question {}.".format(question_id)
    return HttpResponse(response)


def vote(request, question_id):
    return HttpResponse("You're voting on question {}.".format(question_id))
