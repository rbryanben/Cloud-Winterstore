======================================
Cloud Winterstore Admin SDK v0.0.1
======================================

We have put a lot of effort to make Cloud Winterstore very easy to use, both in the application and the documentation. 
Our motto being to secure files and secure them easily.

Storage for your application can be implemented in 2 ways. 
1)	The client can fetch the file they want independently from the Storage Server.
2)	The client requests to the server, and the server retrieves the file for the client from the Storage Server.

The Admin SDK (This Library) is meant for storage implementation using option (1)
This SDK should not be used on the client side as it gives them Administrative Priviledges

======================================
Getting Started
======================================
We assume you have already created an account with us on https://cloudwinterstore.co.zw
(0) Load the Console
(1) Start of by creating a new project
(2) Navigate to the "Accounts Tab"
(3) Click "Admin Accounts"
(4) Create an Admin Account with a strong password
         - You could skip this step if you want to use your own credentials,
            but we do however recommend creating an Admin Account

======================================
Install the Library
======================================
In your terminal, run 

(1) python pip install winterstore-admin

======================================
Test Gateway
======================================
Import the library and use the checkGateWay() method

    import winterstore-admin

    winterstore-admin.checkGateWay()


======================================
Methods
======================================

#
# Check Gateway: Is used to check if the server gateway is open
# Response Types:
#                JSON -- containing server details
checkGateWay()


# 
# Authenticate: Is used to authenticate with the server given a JSON input of type containing
#              username: your_username
#              password: your_password
# Response Types:
#               200 -- success
#               500 -- fail
authenticate(username,password)


#
# Check Authentication: Checks if authenticated
# Response Types:
#               200 -- authenticated 
#               500 -- not authenticated
checkAuthentication()


# Get Folder : Given the project name and the folder identification
#              returns a list of files that belong to the folder in that project
#              as a JSON (API CALL)
# Response Types : 
#                   500 -- means we failed to find the folder you are looking for
#                   denied -- means you do not have access to that folder
#                   JSON[] -- success
getFolder(projectName,id="root")


# Get Path : Given a project name and a path 
#              returns a list of files that belong to the folder in that project
#              as a JSON (API CALL)
# Response Types : 
#                   500 -- means we failed to find the folder you are looking for
#                   denied -- means you do not have access to that folder
#                   Invalid Path -- the path supplied is invalid
#                   Not Folder -- the path supplied leads to a file and not a folder
#                   JSON[] -- success
getPath(projectName,path="root")

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
uploadFile(file,allowAllUsersWrite,allowAllUsersRead,allowKeyUsersWrite,allowKeyUsersRead,name,project,parent)


# Get File: Returns a streaming file given JSON containing the id if a file
# Response Types: 
#                denied -- user is not allowed to read the file
#                500 -- failed
#                   StreamingHttpResponse -- success
getFile(id)


# Get File Using Path : Given a project name and a path 
#              returns a file
# Response Types : 
#                   500 -- means we failed to find the file you are looking for
#                   denied -- means you do not have access to that folder
#                   Invalid Path -- the path supplied is invalid
#                   Not File -- the path supplied leads to a folder and not a file
#                   StreamingHttpResponse -- success
getFileUsingPath(projectName,path)


# File Info : Given a file id 
#              returns infomation on a file
#              as a JSON (API CALL)
# Response Types : 
#                   500 -- means we failed to find the file you are looking for
#                   denied -- means you do not have access to that folder
#                   Invalid Path -- the path supplied is invalid
#                   Not File -- the path supplied leads to a folder and not a file
#                   StreamingHttpResponse -- success
getFileInfo(id)

# 
# Delete : Deletes an index object given the id of the object as JSON Data. 
# Response Types:
#                  Hey! This does'nt look like the json file we need -- The JSON supplied is invalid
#                  Not Found -- the file index object specified was not found
#                  denied -- user does not have pemmision to delete the index object
#                  200 -- success
deleteIndexObject(id)

# Rename : Renames an index object given the objects id and new name as JSON data
# Response Types: 
#           Does'nt seem like the JSON we need -- supplied JSON is invalid
#           Object not found -- object to rename was not found
#           denied -- the user does not have access to write that file
#           1703 -- the new name already exists in that directory 
#           500 -- Failed
rename(id,new_name)


# Give Key : Gives a key to a client to access a files given JSON data with the clients account
#            and the id of the index object to give access to
# Response Types: 
#            not found -- the file/folder specified does not exists
#            500 -- an error occured on our end
#            denied -- user does not have access to write that file
#            200 -- success
giveKey(account,file_id)


# Remove Key: Removes a key from a client given JSON data with 
#             file -- identification of the file
#             accounts [] -- a list for accounts to remove
# Response Types :
#              not found -- file/folder specified was not found
#              500 -- error occured on our side
#              deined -- user does not have access to that file
#              200 - success 
removeKey(accounts,file_id)

# New Folder: Creates a new folder in a project given JSON data containing
#             folderName -- the name of the folder
#             projectName -- the name of the project to create the folder in
#             parentID -- the id of the folder's parent
# Response Types:
#             500 -- failed
#             1701 -- A folder exists under that name
#             denied -- User does not have access to write in the project
#             200 -- success
newFolder(projectName,parentID,folderName)


# Get People With Key : Returns a JSON list of people who have access to a file/folder given JSON data 
#                       that contains the identification of the file/folder
# Response Types:
#                not found -- index object was not found
#                Doesn't look like the JSON we need -- invalid JSON data
#                denied -- the user does not have access to write the file
#                JSON[] -- the users with keys to the file
getPeopleWithKey(id)


# Add Client: Implemented using a POST method, it adds a developer client to a project given JSON data 
#             containing the  identification,password and integration to add to
addClient(identification,integration,password,project)


# Delete Client: Implemented using a POST method, it adds a developer client to a project given JSON data 
#             containing the  identification,password and integration to add to
deleteClient(identification,integration,password,project)


#
# Search Developer Client: returns a JSON list of developers that meet a criteria given JSON data
#                          containing a project.
# Response Types:
#                 not found -- the project was not found
#                 denied -- user does not have access to that project
#                 Does'nt seem like the JSON we need -- invalid JSON data
#                 Json[] -- list of developer clients matching criteria     
searchClient(criteria,project)

#
# Barn Client: barns a developer client account given JSON data containing
#              project and identification
# Response Types:
#               not found -- project || client to barn was not found 
#               500 -- an error occured on our side
#               denied -- user does not have access to perform task
#               200 -- success
banClient(idetification,project)



# Remove Barn: remove barn inflicted on a developer account given JSON data containing 
#              project and identification of developer client to unbarn
# Response Types:
#               not found -- project || client to remove barn was not found 
#               500 -- an error occured on our side
#               denied -- user does not have access to perform task
#               200 -- success  
unbanClient(idetification,project)