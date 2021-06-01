from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from SharedApp.models import Project

@login_required(login_url='/')
def console(request):

    context = {
        "projects" : Project.objects.all()
    }
    return render(request,"Console/console.html",context)




class dummyProject:
    def __init__(self,owner,name) -> None:
        self.owner = owner
        self.name = name