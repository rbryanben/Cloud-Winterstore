from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.db.models import indexes
from django.db.models.base import Model
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.query import FlatValuesListIterable
import random
import string

from datetime import datetime

# The following classes are  store on the SQL Database


#class helper methods
def string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#Accounts classes 
class Project(models.Model):
    owner = models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(auto_now=True,null=False)
    name = models.CharField(max_length=20,null=False)


class Developer(models.Model):
    user = models.OneToOneField(User,null=False,on_delete=models.CASCADE)



class DeveloperClient(models.Model):
    user = models.ForeignKey(User,null=False,on_delete=models.CASCADE)



class BarnedDeveloperClient(models.Model):
    project = models.ForeignKey(Project,null=False,on_delete=models.CASCADE)
    client = models.ForeignKey(DeveloperClient,null=False,on_delete=models.CASCADE)

    def create(self,project,client):
        self.project = project
        self.client = client


#System classes 

class Notification(models.Model):
    project = models.ForeignKey(Project,null=False,on_delete=models.CASCADE)
    body = models.TextField(null=False,blank=False,default="Notification Text")
    read = models.BooleanField(null=False,default=False)
    created = models.DateTimeField(null=False,auto_now=True)

    #constructor
    def create(self,project,body):
        self.project = project
        self.body = body
        self.save()


#Integrations classes 

class Platform(models.Model):
    name = models.TextField(null=False,primary_key=True)


class Integration(models.Model):
    identifier = models.CharField(max_length=25,null=False)
    platform = models.ForeignKey(Platform,on_delete=models.CASCADE,null=False)
    enabled = models.BooleanField(null=False,default=False)
    created = models.DateTimeField(null=False,auto_now=True)
    project = models.ForeignKey(Project,null=False,on_delete=models.CASCADE)
    integrationKey = models.CharField(max_length=64,null=False)


    def create(self,identifier,platform,project):
        self.identifier = identifier
        self.platform = platform
        self.project = project
        self.integrationKey = string_generator(size=64)
        self.save()

    def enable(self):
        self.enabled = True
        self.save()
    
    def disable(self):
        self.enabled = False
        self.save()


class DeletedIntegration(models.Model):
    integration = models.OneToOneField(Integration,null=False,on_delete=models.CASCADE)
    deleted = models.DateTimeField(null=False,auto_now=True)

    def create(self,integration):
        self.integration = integration
        self.save()


#User Key

class FileKey(models.Model):
    file = models.TextField(null=False)
    user = models.ForeignKey(User,null=False,on_delete=models.CASCADE)

    def create(self,file,user):
        self.file = file 
        self.user = user
        self.save()



class DownloadStat(models.Model):
    file = models.TextField(null=False)
    accessed = models.DateTimeField(auto_now=True,null=False)
    accessedBy = models.ForeignKey(User,null=False,on_delete=models.CASCADE)

    def create(self,file,accessed,accessedBy):
        self.file = file
        self.accessed = accessed
        self.accessedBy = accessedBy
        self.save()


class deletedFile(models.Model):
    file = models.TextField(null=False)
    deleted = models.DateTimeField(auto_now=True,null=False)

    def create(self,file):
        self.file = file
        self.save()


class StorageSettings(models.Model):
    project = models.OneToOneField(Project,null=False,primary_key=True,on_delete=models.CASCADE)
    allowUserRead = models.BooleanField(null=False,default=True)
    allowUserWrite = models.BooleanField(null=False,default=True)
    allowAccessControl = models.BooleanField(null=False,default=True)

    def create(self,project,allowUserRead,allowUserWrite,allowAccessControl):
        self.project = project
        self.allowUserRead = allowUserRead
        self.allowUserWrite = allowUserWrite
        self.allowAccessControl = allowAccessControl




#storage classes
class Folder():
    def __init__(self,id,owner,name):
        self.id =id
        self.owner = owner
        self.name =name
        self.created = datetime.now()
        self.collection = []
    
    def getSize(self):
        return 100
    
    def delete(self):
        self.delete()
    
    def getCollectionObject(self,index):
        return self.collection[index]
    
    def getObjectCount(self):
        return len(self.collection) 


class File():
    def __init__(self,id,name,fileReference,type,owner,size,allowAllUsersWrite,allowAllUsersRead,allowKeyUsersWrite,allowKeyUsersRead):
        self.id = id
        self.name =name
        self.fileReference = fileReference
        self.type = type
        self.owner = owner
        self.uploaded = datetime.now()
        self.size = size
        self.allowAllUsersWrite = allowAllUsersWrite
        self.allowAllUsersRead = allowAllUsersRead
        self.allowKeyUsersWrite = allowKeyUsersWrite
        self.allowKeyUsersRead = allowKeyUsersRead
    
    def getSize(self):
        return self.size
    
    def delete(self):
        self.delete
    
    def getFile(self):
        pass 

    def checkIntegrity(self):
        pass

