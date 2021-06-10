from Console.views import console
import json
from django import http
from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from datetime import datetime
from SharedApp.models import IndexObject
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


def deleteIndexObject(request):
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
        destroyIndexObject(objectToDelete)
        return HttpResponse("200")

    #if folder delete object cause it has no file in Mongo
    #but now there is a problem which is to delete all children belonging to the parent object
    if (objectToDelete.objectType == "FD"):
        using = "default"
        nested_objects = NestedObjects(using)
        nested_objects.collect([objectToDelete])
        print(nested_objects.nested())

    return HttpResponse("200")


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

