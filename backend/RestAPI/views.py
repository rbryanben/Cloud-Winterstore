from distutils.util import strtobool
from io import BytesIO
from math import trunc
from os import name
from typing import Sized
from bson.binary import UUID_REPRESENTATION_NAMES
from pymongo.common import BaseObject
from pymongo.message import _randint
from rest_framework.exceptions import NotFound
from Console.views import console
import json
from django import http
from django.http import response
from django.http.response import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from datetime import datetime
from SharedApp.models import BarnedDeveloperClient, Developer, DeveloperClient, IndexObject, Project, TeamCollaboration ,FileKey , deletedFile
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
from  SharedApp.mongohelper import mongoGetFile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate , login
from django.db.models import Q
from Console.models import FileDownloadInstance

#rest framework permmisions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

#storage 
from django.core.files.storage import FileSystemStorage


#streaming 
import os
import re
import mimetypes
from wsgiref.util import FileWrapper
from django.http.response import StreamingHttpResponse
import uuid


#streaming class
range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data

@csrf_exempt
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

# Get People With Key : Returns a JSON list of people who have access to a file/folder given JSON data 
#                       that contains the identification of the file/folder
# Response Types:
#                not found -- index object was not found
#                Doesn't look like the JSON we need -- invalid JSON data
#                denied -- the user does not have access to write the file
#                JSON[] -- the users with keys to the file
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

# Get Deleted Objects: give JSON data containing the project name,
#                      returns a List of deleted objects
# Response Types:
#                 not found -- the project was not found
#                 denied -- user does not have access to a project
#                 500 - an error occured on our side
@login_required(login_url='/console/login-required')
def getDeletedObjectsForProject(request):
    project = None

    try:
        receivedJSON = json.loads(request.body)
        #trim the project to get the project name itself
        projectName = receivedJSON['project'].split(".")[1]
        #get the project owner
        owner = User.objects.get(username=receivedJSON['project'].split(".")[0])
        project = Project.objects.get(owner=owner,name=projectName)
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("not found")
    except:
        return HttpResponse("500")

    #check permmissions
    if (not isAdministrator(request,project)):
        return HttpResponse("denied")

    #get 1000 deleted projects 
    deletedFiles = deletedFile.objects.filter(project=project)[:1000]
    serializerObject = serializers.DeletedFileSerializer(deletedFiles,many=True)

    return JsonResponse(serializerObject.data,safe=False)

@login_required(login_url='/console/login-required')
def getDeletedObjectsForProjectWithCriteria(request):
    project = None
    criteria = None

    try:
        receivedJSON = json.loads(request.body)
        #trim the project to get the project name itself
        projectName = receivedJSON['project'].split(".")[1]
        #get the project owner
        owner = User.objects.get(username=receivedJSON['project'].split(".")[0])
        project = Project.objects.get(owner=owner,name=projectName)
        #get criteria
        criteria = receivedJSON['criteria']
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("not found")
    except:
        return HttpResponse("500")


    #check permmissions
    if (not isAdministrator(request,project)):
        return HttpResponse("denied")

    #get 1000 deleted projects 
    deletedFiles = deletedFile.objects.filter(project=project,fileID=criteria)

    serializerObject = serializers.DeletedFileSerializer(deletedFiles,many=True)

    return JsonResponse(serializerObject.data,safe=False)

# Give Key : Gives a key to a client to access a files given JSON data with the clients account
#            and the id of the index object to give access to
# Response Types: 
#            not found -- the file/folder specified does not exists
#            500 -- an error occured on our end
#            denied -- user does not have access to write that file
#            200 -- success
@login_required(login_url='/console/login-required')
def giveKey(request):
    account = None
    indexObject = None

    try:
        receivedJSON = json.loads(request.body)
        #get developer
        clientToGiveKey = DeveloperClient.objects.get(identification=receivedJSON['account'])
        account = clientToGiveKey.user
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

# Get or Set Access Control: This method either gets the access control values or set them
# Get: Implemented using the POST method, it returns the values given the id of the file or object
#       as JSON data
# Get Response Types:
#       not found -- file/folder was not found
#       Doesn't look like the JSON we need -- supplied JSON is invalid
#       denied -- user does not have access to write the file
#       JsonResponse containing
#                'allowAllUsersWrite' : boolean,
#                'allowAllUsersRead' : boolean,
#                'allowKeyUsersRead' : boolean,
#                'allowKeyUsersWrite' : boolean
# Set: Implemented using the PUT method, updates the access control measures of an index object
#       given JSON data that contains keys
#          'AUW'
#          'AUR'
#          'AKR'
#          'AKW'
# Response types:
#                not found -- object was not found
#                woahh -- does'nt seem like the data we need  -- invalid JSON data
#                denied -- user does not have access to a file
#                200 -- success 
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

# Remove Key: Removes a key from a client given JSON data with 
#             file -- identification of the file
#             accounts [] -- a list for accounts to remove
# Response Types :
#              not found -- file/folder specified was not found
#              500 -- error occured on our side
#              deined -- user does not have access to that file
#              200 - success 
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
            #get developer client user
            userToRemove = DeveloperClient.objects.get(identification=email).user
            FileKey.objects.filter(file=indexObject,user=userToRemove).delete()
        except:
            pass
    
    return HttpResponse("200")

# Rename : Renames an index object given the objects id and new name as JSON data
# Response Types: 
#           Does'nt seem like the JSON we need -- supplied JSON is invalid
#           Object not found -- object to rename was not found
#           denied -- the user does not have access to write that file
#           1703 -- the new name already exists in that directory 
#           500 -- Failed
@login_required(login_url='/console/login-required')
def renameIndexObject(request):
    #presets
    objectID = None
    newName = None

    # extract the objectID and the new name to assign
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


    #check if folder name is not less that
    if (len(folderName) < 3):
        return HttpResponse("500")
    
    #if parent object is not root
    if (parentID != "root"):
        parentObject = IndexObject.objects.get(id=parentID)
    
    #if parent object is root
    if (parentID == "root"):
        parentObject = IndexObject.objects.get(name=projectName)

    #check if similar name exists in parent
    try:
        IndexObject.objects.get(parent=parentObject,name=folderName)
        return HttpResponse("1701")
    except:
        pass
    
    #at this point create an index object 
    newFolder = IndexObject()

    #get project name
    project = projectName.split(".")[1]

    newFolder.create(request.user,"FD",folderName,Project.objects.get(owner=request.user,name=project),parentObject)

    return HttpResponse("200")

# Delete : Deletes an index object given the id of the object as JSON Data. 
# Response Types:
#                  Hey! This does'nt look like the json file we need -- The JSON supplied is invalid
#                  Not Found -- the file index object specified was not found
#                  denied -- user does not have pemmision to delete the index object
#                  200 -- success
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

    # check if person who deleted file was a client 
    developerClient = None
    try:
        developerClient = DeveloperClient.objects.get(user=request.user).identification
    except:
        pass

    # If file, delete the file and respond with 200
    # A file constists of 2 parts, the index object in SQL and the file in mongo 
    # If the file is a startup file, then delete the index object only
    if (objectToDelete.objectType == "FL"):
        #Check if file is a startup file
        if (objectToDelete.fileReference == "HUJDKMEBEJN2G456SGTYINGHT6782HBCDHETYUSHJTIONH7890IFHGR678HNGJOT"or objectToDelete.fileReference == "HYU789IUJ87YHUYT67YGVCFDSER456YTGVBNMKJIKJJ8UUY76TTTFDSER543EFRT"):
            # keep record of deleted record 
            newDeletedFile = deletedFile()
            # decides who deleted file developer or client
            # developer and client are not stored as the same model
            if (developerClient != None):
                #store the record with the client's username
                newDeletedFile.create(objectToDelete.name,developerClient,developerClient,objectToDelete.id,objectToDelete.project)
            else:
                #store the record with the developers username
                newDeletedFile.create(objectToDelete.name,request.user.username,objectToDelete.owner.username,objectToDelete.id,objectToDelete.project)
            
            #delete the object
            objectToDelete.delete()
            #return success
            return HttpResponse("200")

        #The file is not a startup file hence delete the mongo file and the SQL record
        destroyIndexObject(objectToDelete,request,developerClient=developerClient)
        return HttpResponse("200")

    #If folder, delete object cause it has no file in Mongo
    #    but now there is a problem which is to delete all children belonging to the parent object
    #       hence we call the delete folder method
    if (objectToDelete.objectType == "FD"):
        deleteFolder(objectToDelete,request)

    return HttpResponse("200")


####################################################################################
##### Used by client libraries

#
# Get Token: returns a client token given JSON data containing 
#            username and password
# Response Type: 
#               token -- success
#               500 -- failed
@api_view(['POST'])
@csrf_exempt
def getToken(request):
    try:
        receivedJSON = json.loads(request.body)
    except:
        return HttpResponse("Does'nt seem like JSON")
    
    #attempt login
    try:
        user = authenticate(username=receivedJSON["username"], password=receivedJSON["password"])
        if (user is not None):
            login(request, user)
            return HttpResponse(Token.objects.get(user=user).key)
        else:
            return HttpResponse("500")
    except:
         HttpResponse("500")

@api_view(['POST','GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def streamFile(request,slug):
    #get file SQL object
    indexObject = None
    bsonDocumentKey = None
    try: 
        indexObject = IndexObject.objects.get(id=slug)
        bsonDocumentKey  = indexObject.fileReference
    except exceptions.ObjectDoesNotExist:
        
        return HttpResponse("not found")
    except:
        return HttpResponse("500")

    

    #check user is allowed to download the file
    if (not checkPemmission(request,indexObject,"read")):
        return HttpResponse("denied")

    
    #get the file
    fileToStream = None
    try:
        fileToStream = mongoGetFile(bsonDocumentKey)
        #create a new downloadInstance
        newDownloadInstance = FileDownloadInstance()
        newDownloadInstance.create(indexObject,request.user,indexObject.project)
    except:
        return HttpResponse("not found")


    #stream the file
    filename = indexObject.name 
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)

    #create temporary file
    try:
        os.mkdir('temporary_files')
    except:
        pass
    temporaryFile = open('temporary_files/' + indexObject.fileReference,'wb')
    temporaryFile.write(fileToStream.read())
    temporaryFile.close()

    fileToStream.seek(0,2)
    size = fileToStream.tell()
    content_type, encoding = mimetypes.guess_type(filename)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(open('temporary_files/' + indexObject.fileReference,'rb'), offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open('temporary_files/' + indexObject.fileReference,'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp

@api_view(['POST','GET'])
@csrf_exempt
def openStream(request,slug):
    #get file SQL object
    indexObject = None
    bsonDocumentKey = None
    try: 
        indexObject = IndexObject.objects.get(id=slug)
        bsonDocumentKey  = indexObject.fileReference
    except exceptions.ObjectDoesNotExist:
        
        return HttpResponse("not found")
    except:
        return HttpResponse("500")

    
    
    #get the file
    fileToStream = None
    try:
        fileToStream = mongoGetFile(bsonDocumentKey)
    except:
        return HttpResponse("not found")


    #stream the file
    filename = indexObject.name 
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)

    #create temporary file
    try:
        os.mkdir('temporary_files')
    except:
        pass
    temporaryFile = open('temporary_files/' + indexObject.fileReference,'wb')
    temporaryFile.write(fileToStream.read())
    temporaryFile.close()

    fileToStream.seek(0,2)
    size = fileToStream.tell()
    content_type, encoding = mimetypes.guess_type(filename)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(open('temporary_files/' + indexObject.fileReference,'rb'), offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open('temporary_files/' + indexObject.fileReference,'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp


# Download File : Returns a requested file given identification of a file
# Response Type : 
#                 not found -- the file was not found
#                 500 -- an error occured on our end
#                 denied -- the client does not have pemission to that file
#                 Streaming Http Response -- returns the file requested
@api_view(['POST','GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def download(request,slug):
    #get file SQL object
    indexObject = None
    bsonDocumentKey = None
    try: 
        indexObject = IndexObject.objects.get(id=slug)
        bsonDocumentKey  = indexObject.fileReference
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("not found")
    except:
        return HttpResponse("500")

    #check user is allowed to download the file
    if (not checkPemmission(request,indexObject,"read")):
        return HttpResponse("denied")

    
    #get file from mongo 
    try:
        returnedFile = mongoGetFile(bsonDocumentKey)
        
        #create a new downloadInstance
        newDownloadInstance = FileDownloadInstance()
        newDownloadInstance.create(indexObject,request.user,indexObject.project)

        return StreamingHttpResponse(returnedFile,content_type='application/octet-stream')  
    except:
        return HttpResponse("500")


#this method is invalid
@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def getFileWithName(request):
    pathMap = None
    try:
        pathMap = receivedJSON = json.loads(request.body)["path"].split("/")
    except:
        return HttpResponse("Does'nt seem like the json we need")
    
    #store the current directory
    currentDirectory = None

    #iterate the path in pathMap till we get an index object that if not a folder
    for indexItem in pathMap:
        #the root directory is made of 2 variable the <username>.<project>
        #here if the currentDirectory is none that mean we need to assign current derectory to the root folder of 
        #the given project. This is because the root directory name is not the project name
        try:
            if (currentDirectory == None):
                #get the root directory for supplied project
                currentDirectory = IndexObject.objects.get(name=f"{request.user.username}.{indexItem}")
            else:
                currentDirectory = IndexObject.objects.get(name=indexItem)
        except:
            return HttpResponse("not found")  

    #check pemmissions to the currentDirectory 
    if (not checkPemmission(request,currentDirectory,"read")):
        return HttpResponse("denied")

    #if final directoryObject is a folder return msg
    if (currentDirectory.objectType == "FD"):
        return HttpResponse("This is a directory")  
    
    #get file from mongo 
    try:
        returnedFile = mongoGetFile(currentDirectory.fileReference)
        return HttpResponse(returnedFile.read(),content_type='application/octet-stream')  
    except:
        return HttpResponse("500")

#methods to help with some functins
def deleteFolder(folder,request):
    childObject = IndexObject.objects.filter(parent=folder)
    for object in childObject:
        if (object.objectType == "FD"):
            deleteFolder(object)
        else:
            destroyIndexObject(object,request)
    folder.delete()

def destroyIndexObject(object,request, developerClient=None):
    #prevent deletion of startup files
    objectToDelete = object
    if (objectToDelete.fileReference == "HUJDKMEBEJN2G456SGTYINGHT6782HBCDHETYUSHJTIONH7890IFHGR678HNGJOT"or objectToDelete.fileReference == "HYU789IUJ87YHUYT67YGVCFDSER456YTGVBNMKJIKJJ8UUY76TTTFDSER543EFRT"):
        newDeletedFile = deletedFile()
        #check who deleted file developer or client
        if (developerClient != None):
            newDeletedFile.create(objectToDelete.name,developerClient,developerClient,objectToDelete.id,objectToDelete.project)
        else:
            newDeletedFile.create(objectToDelete.name,request.user.username,objectToDelete.owner.username,objectToDelete.id,objectToDelete.project)
        #delete object
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

    #check who deleted file developer or client
    if (developerClient != None):
        newDeletedFile.create(objectToDelete.name,developerClient,developerClient,objectToDelete.id,objectToDelete.project)
    else:
        newDeletedFile.create(objectToDelete.name,request.user.username,objectToDelete.owner.username,objectToDelete.id,objectToDelete.project)
    
    #delete object
    object.delete()

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

def checkPemmission(request,IndexFile,method):
    #check barn
    try:
        developer_client_to_check_barn = DeveloperClient.objects.get(user=request.user)
        project_to_check_barn = IndexFile.project
        BarnedDeveloperClient.objects.get(project=project_to_check_barn,client=developer_client_to_check_barn)
        return False
    except:
        pass
    
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

    #check if permmision is admin
    #the above checks, check if a user is an administrator
    if (method == "admin"):
        return False
    

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

def my_random_string(string_length=128):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.