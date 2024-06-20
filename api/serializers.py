from rest_framework import serializers
from .models import User, File

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_ops_user', 'is_client_user']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # sourcery skip: inline-immediately-returned-variable
        user = User.objects.create_user(**validated_data)
        return user

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'user', 'file', 'uploaded_at']
