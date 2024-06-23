from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UploadedFile

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'is_ops_user', 'is_client_user']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_ops_user=validated_data['is_ops_user'],
            is_client_user=validated_data['is_client_user'],
        )
        return user


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['file', 'uploaded_at', 'file_type']
