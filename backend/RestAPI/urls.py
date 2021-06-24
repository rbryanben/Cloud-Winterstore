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
    path('give-key/',views.giveKey), #remove users with keys
    path('get-deleted-files/',views.getDeletedObjectsForProject), #get deleted files
    path('download/<str:slug>',views.download), #to download a file
]

