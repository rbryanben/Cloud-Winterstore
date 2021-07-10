from os import stat
from rest_framework import fields, serializers
from SharedApp import models
from SharedApp.models import IndexObject , Integration , Platform , DeveloperClient 
from django.contrib.auth.models import User
from .models import FileDownloadInstance , FileDownloadObjectStat

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class IndexObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexObject
        fields = ['id','name']


class FileDownloadInstanceSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    file = IndexObjectSerializer()
    class Meta:
        model = FileDownloadInstance
        fields = ['id','user','downloaded','file','totalDownloads','developerClient']


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ["name"]

class IntegrationSerializer(serializers.ModelSerializer):
    platform = PlatformSerializer()
    class Meta:
        model = Integration
        fields = ["identifier","enabled","created","integrationKey","platform"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","date_joined"]

class DeveloperClientSerializer(serializers.ModelSerializer):
    integration = IntegrationSerializer()
    user = UserSerializer()
    class Meta:
        model = DeveloperClient
        fields = ["integration","identification","user","project","token","last_login","isBarned"]


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['name']