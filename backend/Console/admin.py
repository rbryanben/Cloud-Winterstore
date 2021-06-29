from django.contrib import admin
from .models import FileDownloadInstance , FileDownloadObjectStat

# Register your models here.
admin.site.register(FileDownloadInstance)
admin.site.register(FileDownloadObjectStat)