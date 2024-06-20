from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UploadedFile

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_ops_user', 'is_client_user']

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['file', 'uploaded_at', 'file_type']
