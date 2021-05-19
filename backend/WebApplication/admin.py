from django.contrib import admin
from .models import UnverifiedUser, dummy

# Register your models here.
admin.site.register(UnverifiedUser)
admin.site.register(dummy)
