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
from .models import UnverifiedUser
from random import randint


#landing page
@require_http_methods(["GET",])
def landingPage(request):
    return render(request,"WebApplication/Landing/landing.html")

#Signup page     
@require_http_methods(["GET",])
def signUpPage(request):
    return render(request,"WebApplication/Signup/signup.html")


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
        newUnverifiedUser.create(receivedJSON["username"],receivedJSON["email"],receivedJSON["password"],random_with_N_digits(6))
        sendEmail(newUnverifiedUser.email,newUnverifiedUser.code)
        return HttpResponse("200")
    except:
        return HttpResponse("500")




def sendEmail(email,code):
    sender = 'cloudwinterstore@gmail.com'
    receivers = [email]
    body_of_email = 'Your verification code for Winterstore is ' + str(code)
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
