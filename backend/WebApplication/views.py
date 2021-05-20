from random import randint
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.core import exceptions
import smtplib, ssl
from email.mime.text import MIMEText
import json
import uuid
from .models import UnverifiedUser


#Clicking verification link may not work is I am using SSL
socketSecurity = "http://"

#landing page
@require_http_methods(["GET",])
def landingPage(request):
    return render(request,"WebApplication/Landing/landing.html")

#Signup page     
@require_http_methods(["GET",])
def signUpPage(request):
    return render(request,"WebApplication/Signup/signup.html")


#
#function to verify signed up user
#
@require_http_methods(["GET","POST"])
@csrf_exempt
def verifyUser(request,link):
    #Method POST
    if (request.method == "POST"):
        try:
            receivedJSON = json.loads(request.body)
            receivedUser = UnverifiedUser.objects.get(verificationLink=receivedJSON["link"])
            #if codes dont match return 
            print(receivedJSON["code"])
            if (receivedUser.verificationCode != receivedJSON["code"]):
                return HttpResponse("500")
            #create a new user account
            newUser = User()
            newUser.email = receivedUser.email
            newUser.set_password(receivedUser.password)
            newUser.username = receivedUser.username
            newUser.save()
            #delete unverified user account
            UnverifiedUser.delete(receivedUser)
            #return successfull
            return HttpResponse("200")
        except:
            return HttpResponse("500")
       

    #request is GET  
    try:
        context = {
            "data" : UnverifiedUser.objects.get(verificationLink=link)
        }
        return render(request,"WebApplication/Signup/verification.html",context)
    except:
        return HttpResponse("This is an invalid link")


#
#Function to authanticate user 
#
@csrf_exempt
@require_http_methods(["POST"])
def loginAPI(request):
    receivedJSON = json.loads(request.body)
    #attempt login
    try:
        user = authenticate(username=receivedJSON["username"], password=receivedJSON["password"])
        if (user is not None):
            login(request,user)
            return HttpResponse("200")
        else:
            return HttpResponse("500")
    except:
        return HttpResponse("500")




#
#Function to check if username exists
#
@csrf_exempt
@require_http_methods(["POST"])
def checkUsername(request):
    try:
        receivedJSON = json.loads(request.body)
    except:
        return HttpResponse("did not supply json data")
    #check if username exist
    try:
        User.objects.get(username=receivedJSON["username"])
        return HttpResponse("500")
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("200")

@csrf_exempt 
@require_http_methods(["POST"])
def checkEmail(request):
    try:
        receivedJSON = json.loads(request.body)
    except:
        return HttpResponse("did not supply json data")
    #check if username exist
    try:
        User.objects.get(email=receivedJSON["email"])
        return HttpResponse("500")
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("200")

from django.contrib.sites.shortcuts import get_current_site

@csrf_exempt
@require_http_methods(["POST"])
def NewFreeUserAccount(request):
    try:
        receivedJSON = json.loads(request.body)
    except:
        return HttpResponse("did not supply json data")
    #add to unverified users 
    try:
        newUnverifiedUser = UnverifiedUser()
        newUnverifiedUser.create(receivedJSON["username"],receivedJSON["email"],receivedJSON["password"],random_with_N_digits(6),my_random_string())
        sendEmail(newUnverifiedUser.email,newUnverifiedUser.verificationCode)
        return HttpResponse(newUnverifiedUser.verificationLink)
    except:
        return HttpResponse("500")



def sendEmail(email,code):
    body_of_email =   "Your verification code is " + str(code)
    sender = 'cloudwinterstore@gmail.com'
    receivers = [email]
    msg = MIMEText(body_of_email, 'html')
    msg['Subject'] = "Winterstore Verification"
    msg['From'] = sender
    msg['To'] = ','.join(receivers)
    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = 'cloudwinterstore@gmail.com', password = 'mayday2018')
    s.sendmail(sender, receivers, msg.as_string())
    s.quit()

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def my_random_string(string_length=128):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.
