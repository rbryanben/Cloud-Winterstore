from hashlib import new
import json
from math import trunc
import re
import gridfs
from os import name, truncate
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from pymongo.mongo_client import MongoClient
from distutils.util import strtobool
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

@login_required(login_url='/console/login-required')
@require_http_methods(["POST",])
def uploadFile(request):  
    #get attributes
    uploadedFile = None
    allowAllUsersWrite = None
    allowAllUsersRead = None
    allowKeyUsersRead = None
    allowKeyUsersWrite = None
    name = None
    project = None
    parent = None
    size = None

    try:
        uploadedFile = request.FILES['file'].read()
        allowAllUsersWrite = strtobool(request.POST.get("allowAllUsersWrite"))
        allowAllUsersRead = strtobool(request.POST.get("allowAllUsersRead"))
        allowKeyUsersRead = strtobool(request.POST.get("allowKeyUsersRead"))
        allowKeyUsersWrite = strtobool(request.POST.get("allowKeyUsersWrite"))
        name = request.POST.get("name")
        project = request.POST.get("project")
        parent = request.POST.get("parent")
        size= request.POST.get("size")
    except:
        return HttpResponse("woahh - does'nt seem like the data we need")
    
    #check if folder contains unwanted charectors
    special_characters = "'""!@#$%^&*-+?=,<>/""'"
    if any(c in special_characters for c in name):
        return HttpResponse("1702")

    #check if the username exists in the directory 
    parentIndexObject = None
    try:
        if (parent == "root"):
            parentIndexObject = IndexObject.objects.get(name=f"{request.user.username}.{project}")
        else:
            parentIndexObject = IndexObject.objects.get(id=parent)
    except:
        return HttpResponse("500")

    #check if the filename file exists 
    try:
        IndexObject.objects.get(name=name,parent=parentIndexObject)
        return HttpResponse("1703")
    except:
        pass

    #check if the client as not reached maximum limit 
    #
    #

    try:
        #create an index object 
        newIndexObject = IndexObject()
        newIndexObject.create(request.user,"FL",name,parentIndexObject.project,parentIndexObject,size=size) #create first time to get reference
        
        #upload to mongo
        mongoUploadFile(uploadedFile,newIndexObject.id,name,request.user.username)
    
        #update indexObject
        fileType = "video"
        newIndexObject.fileReference= newIndexObject.id
        newIndexObject.fileType=fileType
        newIndexObject.allowKeyUsersWrite=allowKeyUsersWrite
        newIndexObject.allowKeyUsersRead=allowKeyUsersRead
        newIndexObject.allowAllUsersRead=allowKeyUsersRead
        newIndexObject.allowAllUsersWrite=allowAllUsersWrite
        newIndexObject.save()

        return HttpResponse("200")
    except:
        return HttpResponse("Boss man! something is seriously wrong")

# Create Project API
@require_http_methods(["POST",])
@csrf_exempt
def createProject(request):
    try:
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
    except:
        return HttpResponse("500")

#gets files a folder
@require_http_methods(["POST",])
@login_required(login_url='/console/login-required')
@csrf_exempt
def getFolder(request):
    #get query data
    try:
        receivedJSON = json.loads(request.body)
        projectName = receivedJSON["projectName"]
        folderID = receivedJSON["folderID"]
    
        #folder
        folder = None
        try:
            if (folderID == "root"):
                folder = IndexObject.objects.get(name=f"{request.user.username}.{projectName}")
            else:
                folder = IndexObject.objects.get(id=folderID)

            context = {
                "data" : IndexObject.objects.filter(parent=folder)
            }
        except:
            return HttpResponse("500")

        return render(request,"Console/frames/files.html",context)
    except:
        return HttpResponse("doesn't seem like json data")

@csrf_exempt
@require_http_methods(["POST","GET"])
@login_required(login_url='/console/login-required')
def getFile(request):
    try:
        receivedJSON = json.loads(request.body)
        fileID = receivedJSON['id']
        #get file SQL object 
        indexObject = IndexObject.objects.get(id=fileID)
        bsonDocumentKey  = indexObject.fileReference
        
        #check user is the owner of the project 
        #if not check if the current developer is collaborating in the index object's project
        if (request.user != indexObject.owner):
            #check if there is a collaboration
            try:
                indexObjectProject = indexObject.project
                currentDeveloper = Developer.objects.get(user=request.user)
                TeamCollaboration.objects.get(project=indexObjectProject,developer=currentDeveloper)
            except:
                return HttpResponse("denied")

        #get file from mongo 
        returnedFile = mongoGetFile(bsonDocumentKey)
        return HttpResponse(returnedFile,content_type='application/octet-stream')  
    except:
        return HttpResponse("500") 

def loginRequired(request):
    return HttpResponse("denied")

#mongo helpers 
def mongoGetFile(bsonDocumentKey):
    mongoClient = MongoClient()
    #get bson object with supllied key 
    db = mongoClient["Winterstore"]["Application"]
    bsonObject = db.find_one({"key":bsonDocumentKey})["reference"]
    
    #get file from gridfs
    storageDB = MongoClient()['Winterstore-Storage']
    gridFSConnection = gridfs.GridFS(storageDB)

    #return file
    return gridFSConnection.get(bsonObject).read()

def mongoUploadFile(file,key,filename,owner):
    #upload file to storage
    storageDB = MongoClient()['Winterstore-Storage']
    gridFSConnection = gridfs.GridFS(storageDB)

    #put file 
    referenceObject = gridFSConnection.put(file,filename=filename)

    #store reference object in db 
    mongoClient = MongoClient()
    db = mongoClient["Winterstore"]
    db["Application"].insert_one({
        "owner" : owner,
        "fileName" : filename,
        "reference" : referenceObject,
        "key" : key
    }) 

    return True

#routine for creating a project
def routineNewProject(request,newProject):
    #start a new root index object
    newRootIndexObject = IndexObject()
    newRootIndexObject.create(request.user,"FD",f"{request.user.username}.{newProject.name}",newProject,None)
    #create a new demo file 
    newDemoFile = IndexObject()
    demoFileKey = "HUJDKMEBEJN2G456SGTYINGHT6782HBCDHETYUSHJTIONH7890IFHGR678HNGJOT"
    newDemoFile.create(request.user,"FL","demo.webm",newProject,newRootIndexObject,size=467317,fileReference=demoFileKey,fileType="video",allowKeyUsersWrite=False)
    #create a new demo  folder
    newDemoFolder = IndexObject()
    newDemoFolder.create(request.user,"FD","Media",newProject,newRootIndexObject)
    #create file in new demo folder
    newDemoDocument = IndexObject()
    gettingStartedKey = "HYU789IUJ87YHUYT67YGVCFDSER456YTGVBNMKJIKJJ8UUY76TTTFDSER543EFRT"
    newDemoDocument.create(request.user,"FL","getting-started.pdf",newProject,newDemoFolder,size=34231,fileType="pdf",fileReference="HYU789IUJ87YHUYT67YGVCFDSER456YTGVBNMKJIKJJ8UUY76TTTFDSER543EFRT")

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