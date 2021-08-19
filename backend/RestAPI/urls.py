from django.urls import path , include
from . import views  

urlpatterns = [
    path('gateway/', views.gateway), #gateway
    path('get-token/',views.getToken), #gets token
    path('delete/', views.deleteIndexObject), #delete
    path('new-folder/', views.newFolder), #new folder
    path('rename-object/', views.renameIndexObject), #rename folder
    path('get-people-with-key/',views.getPeopleWithKey), #get people with key
    path('get-set-access-control/',views.getSetAccessControl), #get set access controls
    path('remove-keys/',views.removeKeys), #remove users with keys
    path('give-key/',views.giveKey), #add user with keys
    path('get-deleted-files/',views.getDeletedObjectsForProject), #get deleted files
    path('search-deleted-files/',views.getDeletedObjectsForProjectWithCriteria), #search for deleted files
    path('download/<str:slug>',views.download), #to download a file
    path('get-file/',views.getFileWithName), #gets the file using a path
    path('stream/<str:slug>',views.streamFile), #streams the file

    #for developer demonstration 
    path('open-stream/<str:slug>',views.openStream), #open stream
]

