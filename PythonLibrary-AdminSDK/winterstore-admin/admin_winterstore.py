# Required Imports
import json
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



# 
# Delete : Deletes an index object given the id of the object as JSON Data. 
# Response Types:
#                  Hey! This does'nt look like the json file we need -- The JSON supplied is invalid
#                  Not Found -- the file index object specified was not found
#                  denied -- user does not have pemmision to delete the index object
#                  200 -- success
def deleteIndexObject(id):
    # data to send to the server 
    data = {
        "id" : id
    }

    # delete request
    deleteIndexObjectRequest = SessionConnection.post(serverURL+"/api/delete/",json=data)

    return deleteIndexObjectRequest.text


# Rename : Renames an index object given the objects id and new name as JSON data
# Response Types: 
#           Does'nt seem like the JSON we need -- supplied JSON is invalid
#           Object not found -- object to rename was not found
#           denied -- the user does not have access to write that file
#           1703 -- the new name already exists in that directory 
#           500 -- Failed
def rename(id,new_name):
    # data to send to the server 
    data = {
        "id" : id,
        "name" : new_name
    }

    # send request
    renameRequest = SessionConnection.post(serverURL+"/api/rename-object/",json=data)

    #return 
    return renameRequest.text


# Give Key : Gives a key to a client to access a files given JSON data with the clients account
#            and the id of the index object to give access to
# Response Types: 
#            not found -- the file/folder specified does not exists
#            500 -- an error occured on our end
#            denied -- user does not have access to write that file
#            200 -- success
def giveKey(account,file_id):
    # data to send to the server 
    data = {
        "file" : file_id,
        "account" : account
    }

    # send request
    giveKeyRequest = SessionConnection.post(serverURL+"/api/give-key/",json=data)

    # return
    return giveKeyRequest.text


# Remove Key: Removes a key from a client given JSON data with 
#             file -- identification of the file
#             accounts [] -- a list for accounts to remove
# Response Types :
#              not found -- file/folder specified was not found
#              500 -- error occured on our side
#              deined -- user does not have access to that file
#              200 - success 
def removeKey(accounts,file_id):
    # data to send to the server
    data = {
        "accounts" : accounts,
        "file": file_id
    }

    # remove key request
    removeKeyRequest = SessionConnection.post(serverURL+"/api/remove-keys/",json=data)

    #return the result
    return removeKeyRequest.text


# New Folder: Creates a new folder in a project given JSON data containing
#             folderName -- the name of the folder
#             projectName -- the name of the project to create the folder in
#             parentID -- the id of the folder's parent
# Response Types:
#             500 -- failed
#             1701 -- A folder exists under that name
#             denied -- User does not have access to write in the project
#             200 -- success
def newFolder(projectName,parentID,folderName):
    # data to send 
    data = {
        "projectName" : projectName,
        "parentID" : parentID,
        "folderName" : folderName
    }

    # send request
    newFolderRequest = SessionConnection.post(serverURL+'/api/new-folder/',json=data)

    # return result
    return newFolderRequest.text

# Get People With Key : Returns a JSON list of people who have access to a file/folder given JSON data 
#                       that contains the identification of the file/folder
# Response Types:
#                not found -- index object was not found
#                Doesn't look like the JSON we need -- invalid JSON data
#                denied -- the user does not have access to write the file
#                JSON[] -- the users with keys to the file
def getPeopleWithKey(id):
    # data to send
    data = {
        "id" : id
    }

    # send request
    getPeopleWithKeyRequest = SessionConnection.post(serverURL+"/api/get-people-with-key/",json=data)

    #return response from the server
    return getPeopleWithKeyRequest.text


print(authenticate("test","test"))
