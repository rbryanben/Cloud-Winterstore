from django.contrib import admin
from .models import UnverifiedUser, RecoveryObject , EnhancedSubscription

# Register your models here.
admin.site.register(UnverifiedUser)
admin.site.register(RecoveryObject)
admin.site.register(EnhancedSubscription)

