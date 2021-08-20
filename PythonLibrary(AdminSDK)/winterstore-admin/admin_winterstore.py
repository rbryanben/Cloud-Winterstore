import requests 

##
## Global Session: Keeps the http session because we do not want to lose
##                 authentication data
SessionConnection = requests.session()

##
## Server URL: Keeps the address of the Cloud Winterstore Server
serverURL = "https://cloudwinterstore.co.zw"

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








