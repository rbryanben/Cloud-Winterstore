from django.urls import path
from . import views

urlpatterns = [
    path("",views.landingPage,name="Landing Page") , #Landing Page
    path("login",views.loginAPI), #login
]
