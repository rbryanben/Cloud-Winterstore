from os import name
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

    def create(self,name,owner):
        self.name = name
        self.owner = owner
        self.save()


class Developer(models.Model):
    user = models.OneToOneField(User,null=False,on_delete=models.CASCADE,primary_key=True)

    def create(self,user):
        self.user = user
        self.save()



class DeveloperClient(models.Model):
    user = models.ForeignKey(User,null=False,on_delete=models.CASCADE)



class BarnedDeveloperClient(models.Model):
    project = models.ForeignKey(Project,null=False,on_delete=models.CASCADE)
    client = models.ForeignKey(DeveloperClient,null=False,on_delete=models.CASCADE)

    def create(self,project,client):
        self.project = project
        self.client = client


class TeamCollaboration(models.Model):
    project = models.ForeignKey(Project,null=False,on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer,null=False,on_delete=models.CASCADE)

    def create(self,project,developer):
        try:
            TeamCollaboration.objects.get(project=project,developer=developer)
            return False
        except:
            self.project = project
            self.developer = developer
            self.save()



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
    name = models.TextField(null=False,default="None")
    deletedBy = models.TextField(null=False,default="None")
    owner = models.TextField(null=False,default="None")
    fileID = models.TextField(null=False,default="None")
    deleted = models.DateTimeField(auto_now=True,null=False)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=False,default="")

    def create(self,name,deletedBy,owner,fileID,project):
        self.name = name
        self.deletedBy = deletedBy
        self.owner = owner
        self.fileID = fileID
        self.project = project
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

class IndexObject(models.Model):
    id = models.CharField(null=False,max_length=128,primary_key=True)
    project = models.ForeignKey(Project,null=False,on_delete=models.CASCADE)
    parent = models.ForeignKey('IndexObject',null=True,on_delete=models.CASCADE)
    owner = models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    #object type options 
    OBJECT_TYPE_OPTIONS = [
        ("FD","folder"),
        ("FL","file")
    ]

    objectType = models.CharField(max_length=6,null=False,choices=OBJECT_TYPE_OPTIONS,default="FL")
    name = models.CharField(max_length=64,null=False)
    created = models.DateTimeField(null=False,auto_now=True)
    size = models.IntegerField(null=False,default=0)
    fileReference = models.TextField(null=False)
    fileType = models.CharField(max_length=25)
    allowAllUsersWrite = models.BooleanField(null=False,default=False)
    allowAllUsersRead = models.BooleanField(null=False,default=False)
    allowKeyUsersRead = models.BooleanField(null=False,default=True)
    allowKeyUsersWrite = models.BooleanField(null=False,default=True)

    def getSize(self):
        if (self.objectType == "FD"):
            return self.size
        else:
            return 0
    
    def getFile(self):
        if (self.objectType == "FD"):
            return "should return file"
        else:
            return None

    def checkIntegrety(self):
        return True
    
    def create(self,owner,objectType,name,project,parent, size=0,fileReference="none",fileType="none",allowAllUsersWrite=False,
                allowAllUsersRead=False,allowKeyUsersWrite=True,allowKeyUsersRead=True):
        #generate id
        def getNewID():
            idToAssign = string_generator(64)
            #try and get an object with the generated id, if exception then we can use the id
            try:
                IndexObject.objects.get(id=idToAssign)
                getNewID()
            except:
                return idToAssign
        
        self.id = getNewID()
        self.parent = parent
        self.owner = owner
        self.project = project
        self.objectType = objectType
        self.name = name
        self.size = size
        self.fileReference = fileReference
        self.fileType = fileType
        self.allowAllUsersWrite = allowAllUsersWrite
        self.allowAllUsersRead = allowAllUsersRead
        self.allowKeyUsersRead = allowKeyUsersRead
        self.allowKeyUsersWrite =allowKeyUsersWrite
        self.save()


#User Key
class FileKey(models.Model):
    file = models.ForeignKey(IndexObject,on_delete=models.CASCADE,null=False)
    user = models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    dateObtained = models.DateTimeField(null=False,auto_now=True)
    
    def create(self,file,user):
        self.file = file 
        self.user = user
        self.save()