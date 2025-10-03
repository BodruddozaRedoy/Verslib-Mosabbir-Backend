from rest_framework import serializers
from .models import *

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name','image', 'category']
        read_only_fields = ['code', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SvgSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'image', 'category', 'description', 'code', 'created_at']

