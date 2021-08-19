from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render
from SharedApp.models import IndexObject, Project
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from .views import isAdministrator
from .serializers import IndexObjectSerializer
from SharedApp.mongohelper import mongoGetFile

# Get Folder : Given the project name and the folder identification
#              returns a list of files that belong to the folder in that project
#              as a JSON (API CALL)
# Response Types : 
#                   500 -- means we failed to find the folder you are looking for
#                   denied -- means you do not have access to that folder
#                   JSON[] -- success
@require_http_methods(["POST",])
@login_required(login_url='/console/login-required')
@csrf_exempt
def getFolder(request):
    # Variables to assign the request infomation to
    projectName = None
    folderID = None

    # Extract the project name and folder id from the request
    try:
        receivedJSON = json.loads(request.body)
        projectName = receivedJSON["projectName"]
        folderID = receivedJSON["folderID"]
    except:
        return HttpResponse("doesn't seem like json data")
    
 
    # Variable to store the folder we want to get infomation from
    folder = None
    
    # Get the right folder. 
    # If the folderID is root the assign the folder to be the projects root folder.
    #      this is because the root folder is stored differently from subfolders and files
    # If not, simply assign the folder as the folder with the given folderID
    try:
        if (folderID == "root"):
            # assign root folder 
            folder = IndexObject.objects.get(name=projectName)
        else:
            # assign normal folder
            folder = IndexObject.objects.get(id=folderID)
    except:
        return HttpResponse("Folder Not Found")

    # Check if the user has permission to that folder
    if (not isAdministrator(request,folder.project)):
        return HttpResponse("denied")
    
    # Get the objects in that folder and serialize them 
    folderChildren = IndexObject.objects.filter(parent=folder)
    serializedFolderChildren = IndexObjectSerializer(folderChildren,many=True)

    # Return a list of the children belonging to the folder
    return JsonResponse(serializedFolderChildren.data,safe=False)


# Get Folder : Given a project name and a path 
#              returns a list of files that belong to the folder in that project
#              as a JSON (API CALL)
# Response Types : 
#                   500 -- means we failed to find the folder you are looking for
#                   denied -- means you do not have access to that folder
#                   Invalid Path -- the path supplied is invalid
#                   Not Folder -- the path supplied leads to a file and not a folder
#                   JSON[] -- success
@require_http_methods(["POST",])
@csrf_exempt
@login_required(login_url='/console/login-required')
def getPath(request):
    # Variables to store the path and the project
    projectName = None
    path = None

    # Extract the path and project from the request body
    try:
        receivedJSON = json.loads(request.body)
        projectName = receivedJSON["projectName"]
        path = receivedJSON["path"]
    except:
        return HttpResponse("Does'nt seem like the json we need")
    
    # Split the path into an array so that we can iterate the paths
    pathDirectories = path.split("/")
    
    # Variable to store the current directory, this will eventually become the final directory
    currentDirectory = None
    
    # iterate the path in pathMap till we get the final directory
    try:
        for indexItem in pathDirectories:
            #the root directory is made of 2 variable the <username>.<project>
            #here if the currentDirectory is none that mean we need to assign current derectory to the root folder of 
            #the given project. This is because the root directory name is not the project name
            if (indexItem == "root"):
                # set the currentDirectory as the root
                currentDirectory = IndexObject.objects.get(name=projectName)
            else:
                currentDirectory = IndexObject.objects.get(parent=currentDirectory,name=indexItem)
    # Navigation failed
    except:
        return HttpResponse("Invalid Path")    

    
    # Check if the user has access to the folder 
    if (not isAdministrator(request,currentDirectory.project)):
        return HttpResponse("denied")

    #if final directoryObject is a file return msg
    if (currentDirectory.objectType == "FL"):
        return HttpResponse("Not Folder")  
    
    # get the currentDirectory children and serialize them
    folderChildren = IndexObject.objects.filter(parent=currentDirectory)
    serializedFolderChildren = IndexObjectSerializer(folderChildren,many=True)

    # return JSON List
    return JsonResponse(serializedFolderChildren.data,safe=False)


# Get Folder : Given a project name and a path 
#              returns a files
# Response Types : 
#                   500 -- means we failed to find the file you are looking for
#                   denied -- means you do not have access to that folder
#                   Invalid Path -- the path supplied is invalid
#                   Not File -- the path supplied leads to a folder and not a file
#                   StreamingHttpResponse -- success
@require_http_methods(["POST",])
@csrf_exempt
@login_required(login_url='/console/login-required')
def getFile(request):
    # Variables to store the path and the project
    projectName = None
    path = None

    # Extract the path and project from the request body
    try:
        receivedJSON = json.loads(request.body)
        projectName = receivedJSON["projectName"]
        path = receivedJSON["path"]
    except:
        return HttpResponse("Does'nt seem like the json we need")
    
    # Split the path into an array so that we can iterate the paths
    pathDirectories = path.split("/")
    
    # Variable to store the current directory, this will eventually become the final directory
    currentIndexObject = None
    
    # iterate the path in pathMap till we get the final directory
    try:
        for indexItem in pathDirectories:
            #the root directory is made of 2 variable the <username>.<project>
            #here if the currentDirectory is none that mean we need to assign current derectory to the root folder of 
            #the given project. This is because the root directory name is not the project name
            if (indexItem == "root"):
                # set the currentDirectory as the root
                currentIndexObject = IndexObject.objects.get(name=projectName)
            else:
                currentIndexObject = IndexObject.objects.get(parent=currentIndexObject,name=indexItem)
    # Navigation failed
    except:
        return HttpResponse("Invalid Path")    

    
    # Check if the user has access to the folder 
    if (not isAdministrator(request,currentIndexObject.project)):
        return HttpResponse("denied")

    #if final directoryObject is a folder return msg
    if (currentIndexObject.objectType == "FD"):
        return HttpResponse("Not File")  
    
    #get file from mongo 
    try:
        returnedFile = mongoGetFile(currentIndexObject.fileReference)
        return HttpResponse(returnedFile.read(),content_type='application/octet-stream')  
    except:
        return HttpResponse("500")



# Get Folder : Given a file id 
#              returns infomation on a file
#              as a JSON (API CALL)
# Response Types : 
#                   500 -- means we failed to find the file you are looking for
#                   denied -- means you do not have access to that folder
#                   Invalid Path -- the path supplied is invalid
#                   Not File -- the path supplied leads to a folder and not a file
#                   StreamingHttpResponse -- success
@require_http_methods(["POST",])
@csrf_exempt
@login_required(login_url='/console/login-required')
def fileInfo(request):
    # Variable to store the file identification 
    fileIdentification = None

    # Extract the file identification from the request
    # Extract the path and project from the request body
    try:
        receivedJSON = json.loads(request.body)
        fileIdentification = receivedJSON["id"]
    except:
        return HttpResponse("Does'nt seem like the json we need")

    # Variable to store the indexObject for the file
    fileIndexObject = None
    # Get the indexObject with that identification
    try:
        fileIndexObject = IndexObject.objects.get(id=fileIdentification)
    except:
        return HttpResponse("not found")

    #check if the fileIndexObject is a file
    if (fileIndexObject.objectType == "FD"):
        return HttpResponse("Not File")  

    # Check if the user has access to that file
    if (not isAdministrator(request,fileIndexObject.project)):
        return HttpResponse("denied")
    
    # serialize the object
    serializedIndexObject = IndexObjectSerializer(fileIndexObject)

    #return infomation on the file
    return JsonResponse(serializedIndexObject.data,safe=False)
