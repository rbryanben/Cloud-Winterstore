# Required Imports
import os
import requests 
from requests_toolbelt.multipart import encoder

##
## Global Session: Keeps the http session because we do not want to lose
##                 authentication data
SessionConnection = requests.session()

##
## Server URL: Keeps the address of the Cloud Winterstore Server
serverURL = "http://192.168.1.5"

#
# Check Gateway: Is used to check if the server gateway is open
# Response Types:
#                JSON -- containing server details
def checkGateWay():
    checkGateWayRequest = SessionConnection.get(serverURL+'/api/gateway/')
    return checkGateWayRequest.text

# 
# Authenticate: Is used to authenticate with the server given a JSON input of type containing
#              username: your_username
#              password: your_password
# Response Types:
#               200 -- success
#               500 -- fail
def authenticate(username,password):
    credentials = {
        "username" : username,
        "password" : password
    }
    authenticationRequest = SessionConnection.post(serverURL+'/login',json=credentials)
    return authenticationRequest.text


#
# Check Authentication: Checks if authenticated
# Response Types:
#               200 -- authenticated 
#               500 -- not authenticated
def checkAuthentication():
    checkAuthenticationRequest = SessionConnection.post(serverURL+"/checkAuthentication")
    return checkAuthenticationRequest.text  


# Get Folder : Given the project name and the folder identification
#              returns a list of files that belong to the folder in that project
#              as a JSON (API CALL)
# Response Types : 
#                   500 -- means we failed to find the folder you are looking for
#                   denied -- means you do not have access to that folder
#                   JSON[] -- success
def getFolder(projectName,id="root"):
    # JSON data to send
    data =  {
        "projectName" : projectName,
        "folderID" : id
    }
    # send request
    getFolderRequest = SessionConnection.post(serverURL+"/console/api/get-folder/",json=data)

    #return the response
    return getFolderRequest.text


# Get Folder : Given a project name and a path 
#              returns a list of files that belong to the folder in that project
#              as a JSON (API CALL)
# Response Types : 
#                   500 -- means we failed to find the folder you are looking for
#                   denied -- means you do not have access to that folder
#                   Invalid Path -- the path supplied is invalid
#                   Not Folder -- the path supplied leads to a file and not a folder
#                   JSON[] -- success
def getPath(projectName,path="root"):
    # Data to send to the server
    data = {
        "projectName" : projectName,
        "path" : path
    }

    # Request
    getPathRequest = SessionConnection.post(serverURL+"/console/api/get-path/",json=data)

    # return response
    return getPathRequest.text


#
# Upload File : Uploads a file to a folder in a project given the parameters in multi-part form data.
#               file -- The actual binary file
#               allowAllUsersWrite -- Access control variable
#               allowAllUsersRead -- Access control variable
#               allowKeyUsersWrite -- Access control variable
#               allowKeyUsersRead -- Access control variable
#               name -- The name to store the file as
#               project -- The project the file belongs to, also used to obtain the correct folder to insert to 
#               parent(ID) -- The identification of the parent folder
#               size -- The computed size of the file as bytes by the library (Not Secure - People can bypass)
# Response Types :
#               woahh - does'nt seem like the data we need -- Invalid form data
#               1702 -- name contains unwanted charectors
#               500 -- failed to get the folder to insert to || the user does not have access to the project
#               1703 -- a files exists under that name
#               Boss man! something is seriously wrong -- Failed to save the file
#               200 -- success
def uploadFile(file,allowAllUsersWrite,allowAllUsersRead,allowKeyUsersWrite,allowKeyUsersRead,
                name,project,parent):

    # Compute size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    # Multipart Form data to send
    form = encoder.MultipartEncoder({
        "file": ("file",file, "application/octet-stream"),
        'allowAllUsersWrite' : str(allowAllUsersWrite),
        "allowAllUsersRead" : str(allowAllUsersRead),
        "allowKeyUsersWrite" : str(allowKeyUsersWrite),
        "allowKeyUsersRead" : str(allowKeyUsersRead),
        "name" : name,
        "project" : project,
        "parent" : parent,
        "size" : str(size)
    })

    # Define async Headers
    headers = {"Prefer": "respond-async", "Content-Type": form.content_type}

    # Upload 
    uploadFileRequest = SessionConnection.post(serverURL+"/console/upload-file", headers=headers, data=form)
    
    # return result
    return uploadFileRequest.text
  

# Get File: Returns a streaming file given JSON containing the id if a file
# Response Types: 
#                denied -- user is not allowed to read the file
#                500 -- failed
#                   StreamingHttpResponse -- success
def getFile(id):
    # data to send to server 
    data = {
        "id" : id
    }

    # send 
    getFileRequest = SessionConnection.post(serverURL+"/console/get-file",json=data)

    # return the content
    return getFileRequest.content


# Get File Using Path : Given a project name and a path 
#              returns a file
# Response Types : 
#                   500 -- means we failed to find the file you are looking for
#                   denied -- means you do not have access to that folder
#                   Invalid Path -- the path supplied is invalid
#                   Not File -- the path supplied leads to a folder and not a file
#                   StreamingHttpResponse -- success
def getFileUsingPath(projectName,path):
    # data to send to the server
    data = {
        "projectName" : projectName,
        "path" : path
    }

    # request
    getFileUsingPathRequest = SessionConnection.post(serverURL+"/console/api/get-file/path/",json=data)

    # return file contents
    return getFileUsingPathRequest.content


# File Info : Given a file id 
#              returns infomation on a file
#              as a JSON (API CALL)
# Response Types : 
#                   500 -- means we failed to find the file you are looking for
#                   denied -- means you do not have access to that folder
#                   Invalid Path -- the path supplied is invalid
#                   Not File -- the path supplied leads to a folder and not a file
#                   StreamingHttpResponse -- success
def getFileInfo(id):
    # data to send to the server 
    data = {
        "id" : id
    }

    # request 
    getFileInfoRequest = SessionConnection.post(serverURL+"/console/api/file-info/",json=data)

    # return 
    return getFileInfoRequest.text
