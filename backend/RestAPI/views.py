from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import render
from datetime import datetime


#
# Gateway to chech if the server is online 
#
def gateway(request):
    #for system information
    import platform 
    
    #resopnce JSON 
    response = {
        "Server_Time" : datetime.now(),
        "Operating_System" : platform.system(),
        "Release" : platform.release()
    }

    #return
    return JsonResponse(response)


