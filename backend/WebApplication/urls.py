from django.urls import path
from . import views


urlpatterns = [
    ##############
    ############## Pages
    path("",views.landingPage,name="Landing Page") , #Landing Page
    path("sign-up",views.signUpPage), #Sign Up Page
    
    ##############
    ############## API's
    path("login",views.loginAPI), #login
    path("hjkdjNHjnudellphgy",views.checkUsername), #checks username
    path("hudiueiewfefrefrde",views.checkEmail), #checks email
    
]
