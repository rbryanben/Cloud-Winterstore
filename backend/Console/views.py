from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def console(request):
    return HttpResponse("Console")
