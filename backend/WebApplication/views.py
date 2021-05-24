from datetime import datetime
from random import randint
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators import http
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.core import exceptions
import smtplib, ssl
from email.mime.text import MIMEText
import json
import uuid
from .models import UnverifiedUser ,RecoveryObject


#Clicking verification link may not work is I am using SSL
socketSecurity = "http://"

#landing page
@require_http_methods(["GET",])
def landingPage(request):
    context = {
        "accounts" : len(User.objects.all())
    }
    return render(request,"WebApplication/Landing/landing.html",context)

#Signup page     
@require_http_methods(["GET",])
def signUpPage(request):
    return render(request,"WebApplication/Signup/signup.html")

#
# Abdout page 
def aboutPage(request):
    return render(request,"WebApplication/About/about.html")

#
#documentation page 
def documentation(request):
    return render(request,"WebApplication/Documentation/documentation.html")
#
#recovery page     
@require_http_methods(["GET","POST"])
@csrf_exempt
def recovery(request):
    if (request.method == "POST"):
        try:
            receivedJSON = json.loads(request.body)
            userToRecover = User.objects.get(email=receivedJSON["email"])
            #delete all previous recovery object
            try:
                RecoveryObject.objects.filter(user=userToRecover).delete()
            except:
                pass
            #create a recovery object 
            newRecoveryObject = RecoveryObject()
            newRecoveryObject.create(userToRecover,random_with_N_digits(6),my_random_string())

            #send recovery code
            sendEmailCustomEmail(userToRecover.email,"Your recovery code is "+str(newRecoveryObject.code))
            
            return HttpResponse(newRecoveryObject.slug)
        except:
            return HttpResponse("500")

    #get method
    return render(request,"WebApplication/Recovery/recovery.html")

#
# enhanced page
def enhanced(request):
    return render(request,"WebApplication/Signup/enhanced.html")

#
#recovery page reset
# 
@require_http_methods(["GET","POST"])
@csrf_exempt
def recoveryReset(request,slug):
    try:
        accountToRecover = RecoveryObject.objects.get(slug=slug)
    except:
        return HttpResponse("This is an invalid link") 
    
    #recovery object
    accountToRecover = RecoveryObject.objects.get(slug=slug)

    #post method
    if (request.method == "POST"):
        receivedJSON = json.loads(request.body)
        #check if codes match 
        if (accountToRecover.code != receivedJSON["code"]):
            accountToRecover.failedAttempMade()
            return HttpResponse("500")
        
        #check if password is strong
        if (strongPasswordChecker(receivedJSON["password"]) != 0):
            return HttpResponse("700")

        #change password cause codes matched 
        userAccountToChangePassword = accountToRecover.user

        userAccountToChangePassword.set_password(receivedJSON["password"])
        userAccountToChangePassword.save()

        #delete recovery object
        accountToRecover.delete()

        #logout user
        logout(request)
        
        return HttpResponse("200")

  
    #get method
    # 
    #check if object has not expired
    if (accountToRecover.expired()):
        return HttpResponse("This link has expired") 
    context ={
        "slug" : slug
    }
    return render(request,"WebApplication/Recovery/reset.html",context)
    

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
    
    #check if link exists 
    try:
        receivedUser = UnverifiedUser.objects.get(verificationLink=link)
    except:
        return HttpResponse("This is an invalid link")
    #check expiry
    receivedUser = UnverifiedUser.objects.get(verificationLink=link)
    if (receivedUser.expired()):
        return HttpResponse("This link has expired")
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


@csrf_exempt
@require_http_methods(["POST"])
def NewFreeUserAccount(request):
    try:
        receivedJSON = json.loads(request.body)
    except:
        return HttpResponse("did not supply json data")
    
    #check for injections
    usernameToCheck = receivedJSON["username"]
    email = receivedJSON["email"]
    password = receivedJSON["password"]

    #check username meets standard
    if (not checkUsernameValidation(usernameToCheck)):
        return HttpResponse("500")

    #check password meets standard 
    if (strongPasswordChecker(password) != 0):
        return HttpResponse("500")
    
    #check email 
    if (not checkEmailValid(email)):
        return HttpResponse("500")

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

def sendEmailCustomEmail(email,body_of_email):
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


def strongPasswordChecker(s):
      missing_type = 3
      if any('a' <= c <= 'z' for c in s): missing_type -= 1
      if any('A' <= c <= 'Z' for c in s): missing_type -= 1
      if any(c.isdigit() for c in s): missing_type -= 1
      change = 0
      one = two = 0
      p = 2
      while p < len(s):
         if s[p] == s[p-1] == s[p-2]:
            length = 2
            while p < len(s) and s[p] == s[p-1]:
               length += 1
               p += 1
            change += length / 3
            if length % 3 == 0: one += 1
            elif length % 3 == 1: two += 1
         else:
            p += 1
      if len(s) < 6:
         return max(missing_type, 6 - len(s))
      elif len(s) <= 20:
         return max(missing_type, change)
      else:
         delete = len(s) - 20
         change -= min(delete, one)
         change -= min(max(delete - one, 0), two * 2) / 2
         change -= max(delete - one - 2 * two, 0) / 3
         return delete + max(missing_type, change)

def checkUsernameValidation(username):
    #check length
    if (len(username) < 6):
        return False
    #check existance
    try:
        User.objects.get(username=username)
        return False
    except:
        pass
    
    #check space 
    if (" " in username):
        return False

    #return true if it passes
    return True


def checkEmailValid(email):
    try:
        User.objects.get(email=email)
        return False
    except:
        return True