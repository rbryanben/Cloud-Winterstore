from django.urls import path
from . import views


urlpatterns = [
    ##############
    ############## Pages
    path("",views.console,name="Console") , #Landing Page


    ##############
    ##############REST API
    path("create-project",views.createProject),
    path("get-folder",views.getFilesAndFoldersIn),
]