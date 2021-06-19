from distutils.util import strtobool
from math import trunc
from os import name
from pymongo.common import BaseObject
from rest_framework.exceptions import NotFound
from Console.views import console
import json
from django import http
from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from datetime import datetime
from SharedApp.models import Developer, IndexObject, Project, TeamCollaboration ,FileKey , deletedFile
from django.contrib.admin.utils import NestedObjects
from django.db import router
from pymongo import MongoClient
import gridfs
from django.contrib.auth.decorators import login_required
from django.core import exceptions
from django.forms.models import model_to_dict
from SharedApp import serializers
from django.contrib.auth.models import User
from django.core import exceptions


#
# Gateway to chech if the server is online 
#
def gateway(request):
    #for system information
    import platform 
    
    #resopnce JSON 
    response = {
        "Server_Time" : datetime.now(),
        "Operating_System" : platform.system(),
        "Release" : platform.release()
    }

    #return
    return JsonResponse(response)

@login_required(login_url='/console/login-required')
def getPeopleWithKey(request):
    indexObject = None
    try:
        receivedJSON = json.loads(request.body)
        indexObject =  IndexObject.objects.get(id=receivedJSON['id'])
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("not found")
    except:
        return HttpResponse("Doesn't look like the JSON we need")
    

    #check permission 
    if (not checkPemmission(request,indexObject,"write")):
        return HttpResponse("denied")
    
    #get all objects for file 
    objects = None
    try:
        objects = FileKey.objects.filter(file=indexObject)
        #serialize responce 
        serializer = serializers.FileKeySerializer(objects,many=True)
        return JsonResponse(serializer.data,safe=False)
    except:
        return HttpResponse({})

@login_required(login_url='/console/login-required')
def getDeletedObjectsForProject(request):
    project = None

    try:
        receivedJSON = json.loads(request.body)
        project = Project.objects.get(owner=request.user,name=receivedJSON['project'])
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("not found")
    except:
        return HttpResponse("500")

    #get 200 deleted projects 
    deletedFiles = deletedFile.objects.filter(project=project)
    print(deletedFiles)
    serializerObject = serializers.DeletedFileSerializer(deletedFiles,many=True)
    print(serializerObject.data)
    
    return JsonResponse(serializerObject.data,safe=False)


@login_required(login_url='/console/login-required')
def giveKey(request):
    account = None
    indexObject = None

    try:
        receivedJSON = json.loads(request.body)
        account = User.objects.get(email=receivedJSON['account'])
        indexObject = IndexObject.objects.get(id=receivedJSON['file'])
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("not found")
    except:
        return HttpResponse("500")

    #check permission
    if (not checkPemmission(request,indexObject,"write")):
        return HttpResponse("denied")

    #prevent duplication 
    try:
        FileKey.objects.get(file=indexObject,user=account)
        return HttpResponse("200")
    except:
        pass

    #add a new Key 
    newKey = FileKey()
    newKey.create(indexObject,account)

    return HttpResponse("200")

@login_required(login_url='/console/login-required')
def getSetAccessControl(request):
    if request.method == "POST":
        indexObject = None
        try:
            receivedJSON = json.loads(request.body)
            indexObject =  IndexObject.objects.get(id=receivedJSON['id'])
        except exceptions.ObjectDoesNotExist:
            return HttpResponse("not found")
        except:
            return HttpResponse("Doesn't look like the JSON we need")
        
        #check permission 
        if (not checkPemmission(request,indexObject,"write")):
            return HttpResponse("denied")
        

        return JsonResponse({
                "allowAllUsersWrite" : indexObject.allowAllUsersWrite,
                'allowAllUsersRead' : indexObject.allowAllUsersRead,
                'allowKeyUsersRead' : indexObject.allowKeyUsersRead,
                'allowKeyUsersWrite' : indexObject.allowKeyUsersWrite
        })
    
    if request.method == "PUT":
        #get attributes
        allowAllUsersWrite = None
        allowAllUsersRead = None
        allowKeyUsersRead = None
        allowKeyUsersWrite = None
        indexObject = None
        try:
            receivedJSON = json.loads(request.body)
            allowAllUsersWrite = receivedJSON['AUW']
            allowAllUsersRead = receivedJSON['AUR']
            allowKeyUsersRead = receivedJSON['AKR']
            allowKeyUsersWrite = receivedJSON['AKW']
            indexObject = IndexObject.objects.get(id=receivedJSON['id'])   
        except exceptions.ObjectDoesNotExist:
            return HttpResponse("not found")
        except:
            return HttpResponse("woahh - does'nt seem like the data we need")
        
        #check permission 
        if (not checkPemmission(request,indexObject,"write")):
            return HttpResponse("denied")
        
        #update 
        indexObject.allowAllUsersWrite = allowAllUsersWrite
        indexObject.allowAllUsersRead = allowAllUsersRead
        indexObject.allowKeyUsersRead = allowKeyUsersRead
        indexObject.allowKeyUsersWrite = allowKeyUsersWrite
        indexObject.save()
        
        return HttpResponse("200")

@login_required(login_url='/console/login-required')
def removeKeys(request):
    userList = None
    indexObject = None
    try:
        receivedJSON = json.loads(request.body)
        userList = receivedJSON["accounts"]
        indexObject = IndexObject.objects.get(id=receivedJSON['file'])
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("not found")
    except:
        return HttpResponse("500")
    
    #check permission
    if (not checkPemmission(request,indexObject,"write")):
        return HttpResponse("denied")
    
    #delete users
    for email in userList:
        try:
            FileKey.objects.filter(file=indexObject,user=User.objects.get(email=email)).delete()
        except:
            pass
    
    return HttpResponse("200")

@login_required(login_url='/console/login-required')
def renameIndexObject(request):
    objectID = None
    newName = None

    try:
        receivedJSON = json.loads(request.body)
        objectID = receivedJSON["id"]
        newName = receivedJSON["name"]
    except:
        return HttpResponse("Does'nt seem like the JSON we need")

    #object to rename
    indexObjectToRename = None
    try:
        indexObjectToRename = IndexObject.objects.get(id=objectID)
    except:
        return HttpResponse("Object not found")

    #check permissions
    if (not checkPemmission(request,indexObjectToRename,"write")):
        return HttpResponse("denied")

    #check if the name exists in the current folder 
    parentObject = indexObjectToRename.parent
    try:
        IndexObject.objects.get(parent=parentObject,name=newName)
        return HttpResponse("1703")
    except:
        pass

    #rename object 
    indexObjectToRename.name = newName
    indexObjectToRename.save()

    return HttpResponse("200")

#is not checking permission 
@login_required(login_url='/console/login-required')
def newFolder(request):
    #check if owner of project

    folderName = None
    projectName = None
    parentID = None
    try:
        receivedJSON = json.loads(request.body)
        folderName = receivedJSON['folderName']
        projectName = receivedJSON['projectName']
        parentID = receivedJSON['parentID']
    except:
        return HttpResponse("500")
    

    #parent object container
    parentObject = None
    
    #if parent object is not root
    if (parentID != "root"):
        parentObject = IndexObject.objects.get(id=parentID)
    
    #if parent object is root
    if (parentID == "root"):
        parentObject = IndexObject.objects.get(name=f"{request.user.username}.{projectName}")

    #check if similar name exists in parent
    try:
        IndexObject.objects.get(parent=parentObject,name=folderName)
        return HttpResponse("1701")
    except:
        pass
    
    #at this point create an index object 
    newFolder = IndexObject()
    newFolder.create(request.user,"FD",folderName,Project.objects.get(owner=request.user,name=projectName),parentObject)

    return HttpResponse("200")

@login_required(login_url='/console/login-required')
def deleteIndexObject(request):
    objectID =None
    #try and extract json 
    try:
        receivedJSON = json.loads(request.body)
        objectID = receivedJSON['id']
    except:
        return HttpResponse("Hey! This does'nt look like the json file we need")
    
    #get object to delete
    objectToDelete = None
    try:
        objectToDelete = IndexObject.objects.get(id=objectID)
    except:
        return HttpResponse("Not Found")

    #check if owner of project
    if(not checkPemmission(request,objectToDelete,"write")):
        return HttpResponse("denied")

    #if file delete the file and respind with 200
    if (objectToDelete.objectType == "FL"):
        if (objectToDelete.fileReference == "HUJDKMEBEJN2G456SGTYINGHT6782HBCDHETYUSHJTIONH7890IFHGR678HNGJOT"or objectToDelete.fileReference == "HYU789IUJ87YHUYT67YGVCFDSER456YTGVBNMKJIKJJ8UUY76TTTFDSER543EFRT"):
            #keep record of deleted record 
            newDeletedFile = deletedFile()
            newDeletedFile.create(objectToDelete.name,request.user.username,objectToDelete.owner.username,objectToDelete.id,objectToDelete.project)
            objectToDelete.delete()
            return HttpResponse("200")

        destroyIndexObject(objectToDelete,request)
        return HttpResponse("200")

    #if folder delete object cause it has no file in Mongo
    #but now there is a problem which is to delete all children belonging to the parent object
    if (objectToDelete.objectType == "FD"):
        deleteFolder(objectToDelete,request)

    return HttpResponse("200")

def deleteFolder(folder,request):
    childObject = IndexObject.objects.filter(parent=folder)
    for object in childObject:
        if (object.objectType == "FD"):
            deleteFolder(object)
        else:
            destroyIndexObject(object,request)
    folder.delete()

def destroyIndexObject(object,request):
    #prevent deletion of startup files
    objectToDelete = object
    if (objectToDelete.fileReference == "HUJDKMEBEJN2G456SGTYINGHT6782HBCDHETYUSHJTIONH7890IFHGR678HNGJOT"or objectToDelete.fileReference == "HYU789IUJ87YHUYT67YGVCFDSER456YTGVBNMKJIKJJ8UUY76TTTFDSER543EFRT"):
        newDeletedFile = deletedFile()
        newDeletedFile.create(objectToDelete.name,request.user.username,objectToDelete.owner.username,objectToDelete.id,objectToDelete.project)
        object.delete()
        return

    mongoClient = MongoClient()
    #get bson object with supllied key a, as well as delete it
    db = mongoClient["Winterstore"]["Application"]
    bsonObject = db.find_one({"key":object.fileReference})["reference"]
    #delete reference object
    db.delete_one({"key":object.fileReference})
    
    #get file from gridfs
    storageDB = MongoClient()['Winterstore-Storage']
    gridFSConnection = gridfs.GridFS(storageDB)

    #delete object
    gridFSConnection.delete(bsonObject)

    #delete the indexObject from SQL
    newDeletedFile = deletedFile()
    newDeletedFile.create(objectToDelete.name,request.user.username,objectToDelete.owner.username,objectToDelete.id,objectToDelete.project)
    object.delete()

def checkPemmission(request,IndexFile,method):
    #check if owner of project 
    projectFileObjectBelong =  IndexFile.project
    if (projectFileObjectBelong.owner == request.user):
        return True
    

    #if not the owner check if the user is collborating in the project
    try:
        TeamCollaboration.objects.get(developer=Developer.objects.get(user=request.user),project=projectFileObjectBelong)
        return True
    except:
        pass

    #from here person is a normal user
    userHasKey = False

    #try and obtain key
    try:
        FileKey.objects.get(file=IndexFile,user=request.user)
        userHasKey = True
    except:pass

    if (method == "write"):
        #check if all users can write
        if (IndexFile.allowAllUsersWrite):
            return True
        #if all users can write check if key users can write
        #and if the current user has a key 
        if (IndexFile.allowKeyUsersWrite and userHasKey):
            return True
    
    elif (method == "read"):
        #check if all users can write
        if (IndexFile.allowAllUsersRead):
            return True
        #if all users can write check if key users can write
        #and if the current user has a key 
        if (IndexFile.allowKeyUsersRead and userHasKey):
            return True
    

    #no permission at all
    return False
