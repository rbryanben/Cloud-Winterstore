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

    ###############
    ############### Fallback 
    path("login-required",views.loginRequired), #login required
    path("ds",views.login_required), #test reload
]