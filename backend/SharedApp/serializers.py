from rest_framework import fields, serializers
from .models import FileKey , deletedFile , TeamCollaboration
from SharedApp import models
from django.contrib.auth.models import User
from Console.serializers import UserSerializer as ConsoleUserSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class FileKeySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = FileKey
        fields = ['id','user','dateObtained','developerIdentification'] 
    
class DeletedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = deletedFile
        fields = ['name','deletedBy','owner','fileID','deleted']

class TeamCollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamCollaboration
        fields = ["identification","last_login","added"]