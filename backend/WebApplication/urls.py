from django.urls import path
from . import views


urlpatterns = [
    ##############
    ############## Pages
    path("",views.landingPage,name="Landing Page") , #Landing Page
    path("sign-up",views.signUpPage), #Sign Up Page
    path("verify/<str:link>",views.verifyUser), #to handle verification links
 
    ##############
    ############## API's
    path("login",views.loginAPI), #login
    path("hjkdjNHjnudellphgy",views.checkUsername), #checks username
    path("hudiueiewfefrefrde",views.checkEmail), #checks email
    path("new-free-user",views.NewFreeUserAccount), #new free user
]
