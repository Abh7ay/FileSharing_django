from rest_framework import serializers
from .models import User, File

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_ops_user', 'is_client_user']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        return User.objects.create_user(**validated_data)

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'user', 'file', 'uploaded_at']
