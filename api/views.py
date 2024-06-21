
from django.contrib.auth import authenticate
from django.http import FileResponse, Http404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
import mimetypes

from .models import User, File
from .serializers import UserSerializer, FileSerializer

class UserSignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class FileUploadView(generics.CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FileListView(generics.ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)

class FileDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request, file_id, *args, **kwargs):
        try:
            file = File.objects.get(id=file_id, user=request.user)
        except File.DoesNotExist:
            raise Http404("File not found")

        file_handle = file.file.open()
        file
