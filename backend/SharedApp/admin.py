from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.deletedFile)
admin.site.register(models.Platform)
admin.site.register(models.StorageSettings)
admin.site.register(models.Project)
admin.site.register(models.Notification)
admin.site.register(models.Integration)
admin.site.register(models.FileKey)
admin.site.register(models.DownloadStat)
admin.site.register(models.DeveloperClient)
admin.site.register(models.Developer)
admin.site.register(models.BarnedDeveloperClient)