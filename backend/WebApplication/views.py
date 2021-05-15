from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
import json

# landing page
@require_http_methods(["GET",])
def landingPage(request):
    return render(request,"WebApplication/Landing/landing.html")

@csrf_exempt
@require_http_methods(["POST"])
def loginAPI(request):
    receivedJSON = json.loads(request.body)
    #attempt login
    #try:
    user = authenticate(username=receivedJSON["username"], password=receivedJSON["password"])
    if (user is not None):
        login(request,user)
        return HttpResponse("200")
    else:
        return HttpResponse("500")
    #except:
    return HttpResponse("500")
    
