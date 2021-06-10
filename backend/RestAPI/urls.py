from django.urls import path , include
from . import views

urlpatterns = [
    path('gateway/', views.gateway), #gateway
    path('delete/', views.deleteIndexObject), #delete
]
