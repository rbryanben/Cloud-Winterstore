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
    path('stream/<str:slug>',views.streamFile), #streams the file
    path('create-client-folder',views.createClientFolder), #create client folder
    path('upload-file/',views.clientUploadFile), #Upload A File
    path('client-delete-index-object/',views.clientDeleteIndexObject), # Client Delete Index Object
    path('client-give-key/',views.clientGiveKey), # Client Give Key API
    path('client-remove-keys/',views.clientRemoveKeys), # Client Remove Keys Method
    path('client-file-info/',views.clientFileInfo), # Client Remove Keys Method
    path('client-get-folder/',views.clientGetFolder), # Client Remove Keys Method
 
    #for developer demonstration 
    path('open-stream/<str:slug>',views.openStream), #open stream
]

