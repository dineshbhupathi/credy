from rest_framework import serializers
from .models import *
from requests.auth import HTTPBasicAuth

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'username','date_joined', 'password')

class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ["title","description","genres","uuid"]

class Collectionserializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields= ["title","description","movies","collection_uuid"]


class CollectionGetserializer(serializers.ModelSerializer):
    movies =  MoviesSerializer(many=True,read_only=True)
    class Meta:
        model = Collection
        fields= ["title","description","movies","collection_uuid"]