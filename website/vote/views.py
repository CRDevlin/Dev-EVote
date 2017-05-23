from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .forms import CommentForm


def index(request):
    if request.method == "POST":
        return HttpResponse("Received File")
    else:
        return HttpResponse("Hello, world. You're at the vote index.")
