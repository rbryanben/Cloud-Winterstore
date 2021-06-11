from os import name

from pymongo.common import BaseObject
from Console.views import console
import json
from django import http
from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from datetime import datetime
from SharedApp.models import IndexObject, Project
from django.contrib.admin.utils import NestedObjects
from django.db import router
from pymongo import MongoClient
import gridfs


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


def deleteIndexObject(request):
    #check if owner of project

    objectID =None
    #try and extract json 
    try:
        receivedJSON = json.loads(request.body)
        objectID = receivedJSON['id']
    except:
        return HttpResponse("Hey! This does'nt look like the json file we need")
    
    #get object to delete
    objectToDelete = IndexObject.objects.get(id=objectID)
    

    #if file delete the file and respind with 200
    if (objectToDelete.objectType == "FL"):
        if (objectToDelete.fileReference == "HUJDKMEBEJN2G456SGTYINGHT6782HBCDHETYUSHJTIONH7890IFHGR678HNGJOT"or objectToDelete.fileReference == "HYU789IUJ87YHUYT67YGVCFDSER456YTGVBNMKJIKJJ8UUY76TTTFDSER543EFRT"):
            objectToDelete.delete()
            return HttpResponse("200")

        destroyIndexObject(objectToDelete)
        return HttpResponse("200")

    #if folder delete object cause it has no file in Mongo
    #but now there is a problem which is to delete all children belonging to the parent object
    if (objectToDelete.objectType == "FD"):
        deleteFolder(objectToDelete)

    return HttpResponse("200")


def deleteFolder(folder):
    childObject = IndexObject.objects.filter(parent=folder)
    for object in childObject:
        if (object.objectType == "FD"):
            deleteFolder(object)
        else:
            destroyIndexObject(object)
    folder.delete()

def destroyIndexObject(object):
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
    object.delete()

