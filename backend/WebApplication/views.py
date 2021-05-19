import random
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
from .models import UnverifiedUser, dummy
import string


#Clicking verification link may not work is I am using SSL
socketSecurity = "http://"

#landing page
@require_http_methods(["GET",])
def landingPage(request):
    return render(request,"/Landing/landing.html")

#Signup page     
@require_http_methods(["GET",])
def signUpPage(request):
    return render(request,"/Signup/signup.html")

#
#handle payments 
#
@csrf_exempt
def payments(request):
    receivedJSON = json.loads(request.body)
    print(receivedJSON)
    a = dummy()
    a.data =  receivedJSON
    a.save()
    return HttpResponse("You paynow guys are stupid")
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
        return render(request,"/Signup/verification.html",context)
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


#function called when verification link has been sent
@csrf_exempt
@require_http_methods(["GET"])
def verificationSentLanding(request):
    return render(request,"/Signup/goto_email_verify.html")


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
        newUnverifiedUser.create(receivedJSON["username"],receivedJSON["email"],receivedJSON["password"],verification_link_generator())
        sendEmail(newUnverifiedUser.email,newUnverifiedUser.verificationLink,str(get_current_site(request)))
        return HttpResponse("200")
    except:
        return HttpResponse("500")



def sendEmail(email,linkString,absoluteURL):
    #body
    VerificationLink = socketSecurity + absoluteURL + "/verify/" + linkString 
    body_of_email = "Verify your account by clicking this <a href='"+ VerificationLink +"'>Link</a> or " + VerificationLink  
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

def verification_link_generator(size=128, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
