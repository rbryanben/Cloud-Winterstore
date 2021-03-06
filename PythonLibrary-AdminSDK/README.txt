======================================
Cloud Winterstore Admin SDK v0.0.1
======================================

We have put a lot of effort to make Cloud Winterstore very easy to use, both in the application and the documentation. 
Our motto being to secure files and secure them easily.

Storage for your application can be implemented in 2 ways. 
(1)	The client can fetch the file they want independently from the Storage Server.
(2)	The client requests to the server, and the server retrieves the file for the client from the Storage Server.

The Admin SDK (This Library) is meant for storage implementation using option (1)
This SDK should not be used on the client side as it gives them Administrative Priviledges

======================================
Getting Started
======================================
We assume you have already created an account with us on https://cloudwinterstore.co.zw

(1) Start of by creating a new project
(2) Navigate to the "Accounts Tab"
(3) Click "Admin Accounts"
(4) Create an Admin Account with a strong password
    
======================================
Install the Library
======================================
In your terminal, run 

(1) python pip install winterstore-admin

======================================
Test Gateway
======================================
Import the library and use the checkGateWay() method

    import cloudwinterstore

    cloudwinterstore.checkGateWay()


======================================
Methods
======================================

Check Gateway: Is used to check if the server gateway is open

    checkGateWay()

 
Authenticate: Is used to authenticate with the server

    authenticate(username,password)


Check Authentication: Checks if authenticated

    checkAuthentication()


Get Folder : Get folders

    getFolder(projectName,id="root")


Get Path : returns a list of files that belong to the folder in that project

    getPath(projectName,path="root")


Upload File : Uploads a file to a folder in a project given the parameters in multi-part form data.

    uploadFile(file,allowAllUsersWrite,allowAllUsersRead,allowKeyUsersWrite,allowKeyUsersRead,name,project,parent)


Get File: Returns a streaming file 

    getFile(id)


Get File Using Path : Returns a streaming file
    
    getFileUsingPath(projectName,path)


File Info : Given a file id returns infomation on a file

    getFileInfo(id)


Delete : Deletes an index object.

    deleteIndexObject(id)

Rename : Renames an index object given the objects id and new name as JSON data

    rename(id,new_name)


Give Key : Gives a key to a client to access a files.
    
    giveKey(account,file_id)


Remove Key: Removes a key from a client

    removeKey(accounts,file_id)


New Folder: Creates a new folder in a project

    newFolder(projectName,parentID,folderName)


Get People With Key : Returns a JSON list of people who have access to a file/folder 

    getPeopleWithKey(id)


Add Client: adds a developer client to a project 

    addClient(identification,integration,password,project)


Delete Client: delete a developer client

    deleteClient(identification,integration,password,project)



Search Developer Client: returns a JSON list of developers that meet a criteria 

    searchClient(criteria,project)


Barn Client: barns a developer client Account

    banClient(idetification,project)



Remove Barn: remove barn inflicted on a developer account 

    unbanClient(idetification,project)