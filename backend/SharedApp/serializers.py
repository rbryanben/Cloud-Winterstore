from rest_framework import fields, serializers
from .models import FileKey
from SharedApp import models
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class FileKeySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = FileKey
        fields = ['id','user','dateObtained'] 