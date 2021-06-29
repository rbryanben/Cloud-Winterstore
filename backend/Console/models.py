from RestAPI.views import download
from django.db import models
from SharedApp.models import IndexObject
from django.contrib.auth.models import User


# Create your models here.
class FileDownloadInstance(models.Model):
    file = models.ForeignKey(IndexObject,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    downloaded = models.DateTimeField(auto_now=True)