from django import http
from rest_framework.serializers import Serializer
from SharedApp import serializers
from django.contrib.auth.models import User
from django.core import exceptions
from Console.models import FileDownloadInstance
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
from SharedApp.models import Developer, DeveloperClient, Project , TeamCollaboration, IndexObject , Integration , BarnedDeveloperClient
from .serializers import FileDownloadInstanceSerializer, IntegrationSerializer , DeveloperClientSerializer
from SharedApp.serializers import TeamCollaboratorSerializer


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
    special_characters = "'""!@#$%^&*+?=,<>/""'"
    if any(c in special_characters for c in name):
        return HttpResponse("1702")

    #check if the username exists in the directory 
    parentIndexObject = None
    try:
        if (parent == "root"):
            parentIndexObject = IndexObject.objects.get(name=project)
        else:
            parentIndexObject = IndexObject.objects.get(id=parent)
    except:
        return HttpResponse("500")

    #check pemmision 
    if not isAdministrator(request,parentIndexObject.project):
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
        fileType = "file"
        if (name.endswith(".mp3") or name.endswith(".WAV")):
            fileType = "audio"
        elif (name.endswith(".mp4") or name.endswith(".MOV") or name.endswith(".WMV") or name.endswith(".FLV")  or name.endswith(".MKV")):
            fileType = "video"
        elif (name.endswith(".pdf")):
            fileType = "pdf" 

        newIndexObject.fileReference= newIndexObject.id
        newIndexObject.fileType=fileType
        newIndexObject.allowKeyUsersWrite=allowKeyUsersWrite
        newIndexObject.allowKeyUsersRead=allowKeyUsersRead
        newIndexObject.allowAllUsersRead=allowAllUsersRead
        newIndexObject.allowAllUsersWrite=allowAllUsersWrite
        newIndexObject.save()

        return HttpResponse("200")
    except:
        return HttpResponse("Boss man! something is seriously wrong")

@login_required(login_url='/console/login-required')
@require_http_methods(["POST",])
def getDownloadStats(request):
    #get project name
    project = None
    try:
        receivedJSON = json.loads(request.body)
        #get the user
        projectData = receivedJSON["project"].split(".")
        #user 
        user = User.objects.get(username=projectData[0])
        projectName = projectData[1]
        #assign the project
        project = Project.objects.get(owner=user,name=projectName)
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("not found")
    except:
        return HttpResponse("500")

    #check pemmisions
    if (not isAdministrator(request,project)):
        return HttpResponse("denied")

    #get objects
    downloadObjects = FileDownloadInstance.objects.filter(project=project)
    
    #serialize the data
    serializer = FileDownloadInstanceSerializer(downloadObjects,many=True)
    return JsonResponse(serializer.data,safe=False)


@login_required(login_url='/console/login-required')
@require_http_methods(["POST",])
def searchDownloadStats(request):
    #get project name
    project = None
    criteria = None
    try:
        receivedJSON = json.loads(request.body)
        #criteria
        criteria = receivedJSON["criteria"]
        #get the user
        projectData = receivedJSON["project"].split(".")
        #user 
        user = User.objects.get(username=projectData[0])
        projectName = projectData[1]
        #assign the project
        project = Project.objects.get(owner=user,name=projectName)
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("not found")
    except:
        return HttpResponse("500")

    #check pemmisions
    if (not isAdministrator(request,project)):
        return HttpResponse("denied")

    downloadObjects = []
    #get objects
    try:
        downloadObjects = FileDownloadInstance.objects.filter(project=project,file=IndexObject.objects.get(id=criteria))
    except:
        return HttpResponse("not found")
    
    
    #serialize the data
    serializer = FileDownloadInstanceSerializer(downloadObjects,many=True)
    return JsonResponse(serializer.data,safe=False)

# Create Project API
@require_http_methods(["POST","GET","DELETE","PUT","PATCH"])
@csrf_exempt
@login_required
def projectAdminAccounts(request):
    #POST METHOD
    if (request.method == "POST"):
        project_to_fetch_admin_accounts = None
        try:
            received_json =  json.loads(request.body)
            received_project_data = received_json["project"].split(".")
            received_project_owner  = User.objects.get(username=received_project_data[0])
            received_project_name = received_project_data[1]
            project_to_fetch_admin_accounts = Project.objects.get(owner=received_project_owner,name=received_project_name)
        except:
            return HttpResponse("500")
        
        #check pemmission
        if (not isAdministrator(request,project_to_fetch_admin_accounts)):
            return HttpResponse("denied")

        #get collaborations
        collaborations = TeamCollaboration.objects.filter(project=project_to_fetch_admin_accounts)
        serializer = TeamCollaboratorSerializer(collaborations,many=True)

        #return json objects
        return JsonResponse(serializer.data,safe=False)
    
    #DELETE METHOD
    if (request.method == "DELETE"):
        project_to_delete_admin_accounts = None
        team_collaboration_to_delete = None
        try:
            received_json =  json.loads(request.body)
            received_project_data = received_json["project"].split(".")
            received_project_owner  = User.objects.get(username=received_project_data[0])
            received_project_name = received_project_data[1]
            project_to_delete_admin_accounts = Project.objects.get(owner=received_project_owner,name=received_project_name)
            #get developer
            developer_email = received_json['identification']
            developer = Developer.objects.get(user=User.objects.get(email=developer_email))
            #get admin account to delete
            team_collaboration_to_delete = TeamCollaboration.objects.get(project=project_to_delete_admin_accounts,developer=developer)
        except exceptions.ObjectDoesNotExist:
            return HttpResponse("not found")
        except:
            return HttpResponse("500")
        
        #check pemmission
        if (not isAdministrator(request,project_to_delete_admin_accounts)):
            return HttpResponse("denied")

        team_collaboration_to_delete.delete()
        return HttpResponse("200")

    #PUT METHOD
    if (request.method == "PUT"):
        project_to_add_admin_accounts = None
        developer = None
        try:
            received_json =  json.loads(request.body)
            received_project_data = received_json["project"].split(".")
            received_project_owner  = User.objects.get(username=received_project_data[0])
            received_project_name = received_project_data[1]
            project_to_add_admin_accounts = Project.objects.get(owner=received_project_owner,name=received_project_name)
            #get developer
            developer_email = received_json['identification']
            developer = Developer.objects.get(user=User.objects.get(email=developer_email))
        except exceptions.ObjectDoesNotExist:
            return HttpResponse("not found")
        except:
            return HttpResponse("500")
        
        #check pemmission
        if (not isAdministrator(request,project_to_add_admin_accounts)):
            return HttpResponse("denied")

        #add a new team collaboration
        newCollaboration = TeamCollaboration()
        newCollaboration.create(project_to_add_admin_accounts,developer)

        return HttpResponse("200")


    #PATCH METHOD
    if (request.method == "PATCH"):
        project_to_respond_admin_accounts = None
        developer = None
        try:
            received_json =  json.loads(request.body)
            received_project_data = received_json["project"].split(".")
            received_project_owner  = User.objects.get(username=received_project_data[0])
            received_project_name = received_project_data[1]
            project_to_respond_admin_accounts = Project.objects.get(owner=received_project_owner,name=received_project_name)
            #get developer
            developer_email = received_json['identification']
            developer = Developer.objects.get(user=User.objects.get(email=developer_email))
        except exceptions.ObjectDoesNotExist:
            return HttpResponse("[]")
        except:
            return HttpResponse("500")
        
        #check pemmission
        if (not isAdministrator(request,project_to_respond_admin_accounts)):
            return HttpResponse("denied")
        
        collaborations = None
        try:
            collaborations = TeamCollaboration.objects.filter(project=project_to_respond_admin_accounts,developer=developer)
        except:
            pass
        serializer = TeamCollaboratorSerializer(collaborations,many=True)
        
        return JsonResponse(serializer.data,safe=False)

# Create Project API
@require_http_methods(["POST",])
@csrf_exempt
@login_required
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

@require_http_methods(["POST",])
@csrf_exempt
@login_required
def barnClient(request):
    CLIENT_TO_BARN = None
    PROJECT = None

    #get account to barn
    try: 
        receivedJSON = json.loads(request.body)
        #get project to barn from
        project_to_barn_from_data = receivedJSON['project'].split(".")
        project_to_barn_from_owner = User.objects.get(username=project_to_barn_from_data[0])
        project_to_barn_from_name = project_to_barn_from_data[1]
        PROJECT = Project.objects.get(owner=project_to_barn_from_owner,name=project_to_barn_from_name)
        
        #client to barn
        client_to_barn_identification = receivedJSON['identification']
        CLIENT_TO_BARN = DeveloperClient.objects.get(identification=client_to_barn_identification,project=PROJECT)
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("not found")
    except:
        return HttpResponse("500")

    #check pemmissions to carry out task 
    if (not isAdministrator(request,PROJECT)):
        return HttpResponse("denied")

    # Barn user account
    try:
        barn = BarnedDeveloperClient()
        barn.create(PROJECT,CLIENT_TO_BARN)
    except:
        pass

    return HttpResponse("200")

@require_http_methods(["POST",])
@csrf_exempt
@login_required
def removeBarnForClient(request):
    CLIENT_TO_REMOVE_BARN = None
    PROJECT = None

    #get account to barn
    try: 
        receivedJSON = json.loads(request.body)
        #get project to barn from
        project_to_remove_barn_from_data = receivedJSON['project'].split(".")
        project_to__remove_barn_from_owner = User.objects.get(username=project_to_remove_barn_from_data[0])
        project_to_remove_barn_from_name = project_to_remove_barn_from_data[1]
        PROJECT = Project.objects.get(owner= project_to__remove_barn_from_owner,name=project_to_remove_barn_from_name)
        
        #client to barn
        client_to_remove_barn_identification = receivedJSON['identification']
        CLIENT_TO_REMOVE_BARN = DeveloperClient.objects.get(identification=client_to_remove_barn_identification,project=PROJECT)
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("not found")
    except:
        return HttpResponse("500")

    #check pemmissions to carry out task 
    if (not isAdministrator(request,PROJECT)):
        return HttpResponse("denied")

    # Barn user account
    BarnedDeveloperClient.objects.get(client=CLIENT_TO_REMOVE_BARN).delete()

    return HttpResponse("200")


# Create Project API
@require_http_methods(["POST"])
@csrf_exempt
@login_required
def search_update_integration(request):
    if (request.method == "POST"):
        project = getProjectFromRequest(request)
        criteria = getValueOfJSONRequest(request,"criteria")


        if (not isAdministrator(request,project)):
            return HttpResponse("denied")
       
        objects = Integration.objects.filter(project=project,identifier=criteria)
        data = IntegrationSerializer(objects,many=True)

        return JsonResponse(data.data,safe=False)

# Create Project API
@require_http_methods(["POST"])
@csrf_exempt
@login_required
def integrations(request):
    project = None
    try:
        receivedJSONData = json.loads(request.body)['project'].split(".")
        #project name and user
        username = receivedJSONData[0]
        projectName = receivedJSONData[1]
        project = Project.objects.get(owner=User.objects.get(username=username),name=projectName)
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("not found")
    except:
        return HttpResponse("Does'nt seem like the JSON we need")


    #check if the request is an administrator
    if (not isAdministrator(request,project)):
        return HttpResponse("denied")

    #get integrations
    integrations = Integration.objects.filter(project=project)

    #serialize
    serializer = IntegrationSerializer(integrations,many=True)

    return JsonResponse(serializer.data,safe=False)

@require_http_methods(["POST","PUT"])
@csrf_exempt
@login_required
def developerClient(request):
    if (request.method == "POST"):
        #get project
        project = None

        #assign project
        try:
            receivedJSON = json.loads(request.body)["project"].split(".")
            projectOwnerUsername = receivedJSON[0]
            projectName = receivedJSON[1]
            #get project 
            project = Project.objects.get(owner=User.objects.get(username=projectOwnerUsername),name=projectName)
        except exceptions.ObjectDoesNotExist:
            return HttpResponse("not found")
        except:
            return HttpResponse("Does'nt seem like the JSON we need")
        
        #get developer clients
        developerClients = DeveloperClient.objects.filter(project=project)

        serializer = DeveloperClientSerializer(developerClients,many=True)

        return JsonResponse(serializer.data,safe=False)

def searchDeveloperClients(request):
    #get project
    project = None
    criteria = None

    #assign project
    try:
        receivedJSON = json.loads(request.body)["project"].split(".")
        projectOwnerUsername = receivedJSON[0]
        projectName = receivedJSON[1]
        #criteria
        criteria = json.loads(request.body)["criteria"]

        #get project 
        project = Project.objects.get(owner=User.objects.get(username=projectOwnerUsername),name=projectName)
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("not found")
    except:
        return HttpResponse("Does'nt seem like the JSON we need")
    
    if (not isAdministrator(request,project)):
        return HttpResponse("denied")

    #get developer clients
    developerClients = DeveloperClient.objects.filter(project=project,identification=criteria)
    serializer = DeveloperClientSerializer(developerClients,many=True)

    return JsonResponse(serializer.data,safe=False)

@require_http_methods(["POST","UPDATE","DELETE"])
@csrf_exempt
@login_required
def addDeveloperClient(request):
    client_to_add_identification =None
    client_to_add_password = None
    project_with_integration = None
    integration_to_add_to = None

    #get the data
    try:
        receivedJSON = json.loads(request.body)
        client_to_add_identification = receivedJSON["identification"]
        client_to_add_password = receivedJSON["password"]
        integration_name = receivedJSON["integration"]
        #get project
        data_to_fetch_project = receivedJSON["project"].split(".")
        owner_of_project = User.objects.get(username=data_to_fetch_project[0])
        project_with_integration = Project.objects.get(owner=owner_of_project,name=data_to_fetch_project[1])

        #integration
        integration_to_add_to = Integration.objects.get(project=project_with_integration,identifier=integration_name)
    except:
        return HttpResponse("500")


    #check pemmissions
    if (not isAdministrator(request,project_with_integration)):
        return HttpResponse("denied")

    

    #add a new developer client
    if not meetsHTMLCompatability(client_to_add_identification):
        return HttpResponse("1706")

    
    #UPDATE if request is update
    if (request.method == "UPDATE"):
        try:
            client_to_update = DeveloperClient.objects.get(integration=integration_to_add_to,identification=client_to_add_identification)
            client_to_update.user.set_password(client_to_add_password)
            client_to_update.user.save()
            return HttpResponse("200")
        except:
            return HttpResponse("500")

    #DELET
    if (request.method == "DELETE"):
        try:
            client_to_update = DeveloperClient.objects.get(integration=integration_to_add_to,identification=client_to_add_identification)
            client_to_update.user.delete()
            client_to_update.delete()
            return HttpResponse("200")
        except:
            return HttpResponse("500")
        
        
    
    
    #check if the client exists
    try:
        DeveloperClient.objects.get(identification=client_to_add_identification,integration=integration_to_add_to)
        return HttpResponse("1704")
    except:
        pass

    #create a new Developer Client
    new_developer_client = DeveloperClient()
    new_developer_client.create(integration_to_add_to,project_with_integration,client_to_add_identification,client_to_add_password)

    return HttpResponse("200")

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
                folder = IndexObject.objects.get(name=projectName)
            else:
                folder = IndexObject.objects.get(id=folderID)

            context = {
                "data" : IndexObject.objects.filter(parent=folder)
            }
        except:
            return HttpResponse("500")

        if (not isAdministrator(request,folder.project)):
            return HttpResponse("denied")

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
        if (not isAdministrator(request,indexObject.project)):
            return HttpResponse("denied")

        #get file from mongo 
        returnedFile = mongoGetFile(bsonDocumentKey)

        #create a new downloadInstance
        newDownloadInstance = FileDownloadInstance()
        newDownloadInstance.create(indexObject,request.user,indexObject.project)
        
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

def isAdministrator(request,project):
    #check if owner
    if (project.owner == request.user):
        return True
    
    #if not the owner check if the user is collborating in the project
    try:
        TeamCollaboration.objects.get(developer=Developer.objects.get(user=request.user),project=project)
        return True
    except:
        pass

    return False

def meetsHTMLCompatability(string):
    return True

def getProjectFromRequest(request):   
    try:
        receivedData = json.loads(request.body)
        project_owner_data = receivedData["project"].split(".")
        project = Project.objects.get(owner=User.objects.get(username=project_owner_data[0]),name=project_owner_data[1])
        return project
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("not found")
    except:
        return HttpResponse("500")

def getProjectOwnerFromRequest(request):
    try:
        receivedData = json.loads(request.body)
        project_owner_data = receivedData["project"].split(".")
        return User.objects.get(username=project_owner_data[0])
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("not found")
    except:
        return HttpResponse("500")

def getJSONFromRequest(request):
    try:
        receivedData = json.loads(request.body)
        return receivedData
    except:
        return HttpResponse("500")

def getValueOfJSONRequest(request,key):
    try:
        receivedData = json.loads(request.body)
        return receivedData[key]
    except:
        return HttpResponse("500")

def checkProjectName(request,name):
    if (len(name) < 6):
        return False
    if (" " in name):
        return False
    try:
        Project.objects.get(owner=request.user,name=name)
        return False
    except:
        return True


    def __init__(self,owner,name) -> None:
        self.owner = owner
        self.name = name