from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render
from SharedApp.models import IndexObject
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from .views import isAdministrator
from .serializers import IndexObjectSerializer

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


