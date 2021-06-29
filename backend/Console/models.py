from hashlib import new
from os import stat
from django.db import models
from django.db.models.fields import AutoField
from SharedApp.models import IndexObject, Project
from django.contrib.auth.models import User


class FileDownloadObjectStat(models.Model):
    indexObject = models.OneToOneField(IndexObject,on_delete=models.CASCADE,null=False)
    download = models.IntegerField(default=1)

    def create(self,indexObject):
        self.indexObject = indexObject
        self.save()

    def increment(self):
        self.download += 1 
        self.save()

# Create your models here.
class FileDownloadInstance(models.Model):
    file = models.ForeignKey(IndexObject,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    downloaded = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,default=None)
    
    def create(self,file,user,project):
        self.file = file
        self.user = user
        self.project = project
        self.save()
        #if FileDownload object does not exist create one
        try:
            statsObject = FileDownloadObjectStat.objects.get(indexObject=self.file)
            statsObject.increment()
        except:
            newStatsObject = FileDownloadObjectStat()
            newStatsObject.create(self.file)
    
    @property
    def totalDownloads(self):
        try:
            return FileDownloadObjectStat.objects.get(indexObject=self.file).download
        except:
            return "Error"
    
    