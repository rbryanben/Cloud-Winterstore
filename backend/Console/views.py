import json
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from pymongo.mongo_client import MongoClient
from SharedApp.models import Developer, Project , TeamCollaboration 


@login_required(login_url='/')
def console(request):
    #local useful vars
    currentDeveloper = Developer.objects.get(user=request.user)
    currentUser = request.user

    #max projects 
    maxProjectsReached = False
    if (len(Project.objects.filter(owner=request.user)) >= 5):
        maxProjectsReached = True

    #get all collaborating object 
    teamCollaborations = TeamCollaboration.objects.filter(developer=currentDeveloper)
    collaboratingProjects = []
    
    #assign collaborations - extract from teamCollaborations 
    for object in teamCollaborations:
        collaboratingProjects.append(object.project)


    #final context 
    context = {
        "projects" : Project.objects.filter(owner=request.user),
        "collaboratingProjects" :  collaboratingProjects,
        "maxProjectsReached" : maxProjectsReached
    }
    return render(request,"Console/console.html",context)


# Create Project API
@require_http_methods(["POST",])
@csrf_exempt
def createProject(request):
    receivedJSON = json.loads(request.body)
    newProjectName = receivedJSON["name"]
    
    #check standard
    if (not checkProjectName(request,newProjectName)):
        return HttpResponse("500")
    
    #has 5 projects 
    if (len(Project.objects.filter(owner=request.user)) >= 5):
        return HttpResponse("500")
    
    #create project 
    newProject = Project()
    newProject.create(newProjectName,request.user)

    return HttpResponse("200")


#gets files a folder
@require_http_methods(["POST",])
@csrf_exempt
def getFilesAndFoldersIn(request):
    #get query data
    receivedJSON = json.loads(request.body)
    projectName = receivedJSON["projectName"]
    folderName = receivedJSON["folderName"]

    return render(request,"Console/frames/files.html")

   

def checkProjectName(request,name):
    if (len(name) < 6):
        print("a")
        return False
    if (" " in name):
        print("b")
        return False
    try:
        Project.objects.get(owner=request.user,name=name)
        return False
    except:
        return True


    def __init__(self,owner,name) -> None:
        self.owner = owner
        self.name = name