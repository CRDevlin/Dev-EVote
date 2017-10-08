from django.shortcuts import render
from django.http import HttpResponse

from TasksManager.models import Record

def page(request):
    # If form has posted
    if request.POST:
        if 'token' in request.POST:
            token = request.POST.get('token', '')
            record = Record.objects.get(id=token)
            return HttpResponse("Record Obtained!")
