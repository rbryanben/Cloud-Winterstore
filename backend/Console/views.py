import json
from os import name
import string
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from pymongo.mongo_client import MongoClient
from SharedApp.models import Developer, Project , TeamCollaboration, IndexObject


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

    #run project creation routine
    routineNewProject(request,newProject)

    return HttpResponse("200")


#gets files a folder
@require_http_methods(["POST",])
@csrf_exempt
def getFolder(request):
    #get query data
    receivedJSON = json.loads(request.body)
    projectName = receivedJSON["projectName"]
    folderID = receivedJSON["folderID"]
    
    #folder
    folder = None
    if (folderID == "root"):
        folder = IndexObject.objects.get(name=f"{request.user.username}.{projectName}")
    else:
        folder = IndexObject.objects.get(id=folderID)

    context = {
        "data" : IndexObject.objects.filter(parent=folder)
    }

    return render(request,"Console/frames/files.html",context)

   

#routine for creating a project
def routineNewProject(request,newProject):
    #start a new root index object
    newRootIndexObject = IndexObject()
    newRootIndexObject.create(request.user,"FD",f"{request.user.username}.{newProject.name}",newProject,None)
    #create a new demo file 
    newDemoFile = IndexObject()
    demoFileKey = "HUJDKMEBEJN2G456SGTYINGHT6782HBCDHETYUSHJTIONH7890IFHGR678HNGJOTUI"
    newDemoFile.create(request.user,"FL","demo.webm",newProject,newRootIndexObject,size=467317,fileReference=demoFileKey,fileType="video",allowKeyUsersWrite=False)
    


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