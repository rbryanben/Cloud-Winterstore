import json
import requests 

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
def authenticate(credentials):
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

# Test Authenticate "
print(authenticate({"username" : "test","password" : "test"}))
print("============================================================")
# Test Get Folder
children = json.loads(getFolder("rbryanben.Demo-Project",id="VTITGJMX4T9TAT54P4MVMIWOGB3ZAEUOL0QGVFZ4V4U2DKKF3U8KY5BXSS2FUQZZ"))
for child in children:
    print(child["name"])
print("============================================================")

# Test Get Path
children = json.loads(getPath("test.Demo-Project",path="root/Media/Drama"))
for child in children:
    print(child["name"])

print("============================================================")

