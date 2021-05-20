from django.contrib.auth.models import User
from django.db import models
from django.db.models.base import Model

# unverified users
class UnverifiedUser(models.Model):
    username  = models.TextField(null=False)
    email = models.TextField(null=False,blank=False,primary_key=True)
    password = models.TextField(null=False)
    verificationCode = models.CharField(max_length=6,default="000000",null=False)
    verificationLink = models.CharField(max_length=128,default="not set")
    #constructor
    def create(self,username,email,password,verificatonCode,verificationLink):
        self.username = username
        self.email = email
        self.password = password
        self.verificationCode = verificatonCode
        self.verificationLink = verificationLink
        self.save()


class RecoveryObject(models.Model):
    user = models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    code = models.CharField(max_length=6,null=False,blank=False)
    slug = models.CharField(max_length=128,null=False,default="xxEO1",blank=False)
    attempts = models.IntegerField(default=3,null=False) #if attempts become 0 delete object
    #method to create object
    def create(self,user,code,slug):
        self.user = user
        self.code = code
        self.slug = slug
        self.save()
    
    def failedAttempMade(self):
        self.attempts -= 1 
        self.save()
        if (self.attempts == 0):
            self.delete()
    
