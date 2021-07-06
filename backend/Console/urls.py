from django.urls import path
from . import views


urlpatterns = [
    ##############
    ############## Pages
    path("",views.console,name="Console") , #Landing Page


    ##############
    ##############REST API
    path("create-project",views.createProject), #creates a project
    path("get-folder",views.getFolder), #gets a folder
    path("get-file",views.getFile), #gets a file
    path("upload-file",views.uploadFile), #uploads file
    path("get-download-stats",views.getDownloadStats), #to get download stats
    path("search-download-stats",views.searchDownloadStats), #to get download stats
    path("integrations",views.integrations), #integrations
    path("developer-clients",views.developerClient), #developer clients
    path("barn-client-account",views.barnClient), #barn client
    path("remove-barn-client-account",views.removeBarnForClient), #barn client
    path("search-developer-clients",views.searchDeveloperClients), #search developer client

    ###############
    ############### Fallback 
    path("login-required",views.loginRequired), #login required
    
]