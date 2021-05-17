from enum import Flag
from django.db import models
from django.db.models.base import Model

# unverified users
class UnverifiedUser(models.Model):
    username  = models.TextField(null=False)
    email = models.TextField(null=False,blank=False,primary_key=True)
    password = models.TextField(null=False)
    code = models.CharField(max_length=6,default="000000",null=False)
    #constructor
    def create(self,username,email,password,code):
        self.username = username
        self.email = email
        self.password = password
        self.code = code
        self.save()