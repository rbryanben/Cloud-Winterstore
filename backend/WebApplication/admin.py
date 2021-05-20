from django.contrib import admin
from .models import UnverifiedUser, RecoveryObject

# Register your models here.
admin.site.register(UnverifiedUser)
admin.site.register(RecoveryObject)

