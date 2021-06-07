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


    ###############
    ############### Fallback 
    path("login-required",views.loginRequired), #login required
]