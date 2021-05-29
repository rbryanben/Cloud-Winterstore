from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def console(request):
    return render(request,"Console/console.html")
