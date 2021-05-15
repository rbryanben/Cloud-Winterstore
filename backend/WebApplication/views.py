from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render

# landing page 
def landingPage(request):
    return render(request,"WebApplication/Landing/landing.html")
