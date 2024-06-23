from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import CustomUser, UploadedFile
from .serializers import CustomUserSerializer, UploadedFileSerializer
from django.core.signing import Signer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import FileResponse, Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        verification_code = get_random_string(length=6)
        user.verification_code = verification_code
        user.is_active = False  # Initially set the user to inactive
        user.save()
        send_mail(
            'Verify your email',
            f'Your verification code is {verification_code}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

class VerifyEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')
        try:
            user = CustomUser.objects.get(email=email, verification_code=verification_code)
            user.is_active = True
            user.verification_code = None  # Clear the verification code after successful verification
            user.save()
            return Response({'message': 'Email verified'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Invalid code or email'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if not user.is_active:
                return Response({'message': 'Account is not active'}, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        
class UploadFileView(generics.CreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_ops_user:
            raise PermissionDenied('Only ops users can upload files')
        serializer.save(user=self.request.user)

class ListFilesView(generics.ListAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UploadedFile.objects.filter(user=self.request.user)


class DownloadFileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        try:
            file = UploadedFile.objects.get(id=file_id)
        except UploadedFile.DoesNotExist:
            raise Http404("File not found")

        if not request.user.is_client_user:
            raise PermissionDenied('Only client users can download files')

        response = FileResponse(file.file.open('rb'))
        response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
        return response
    
def generate_download_link(file):
    signer = Signer()
    signed_value = signer.sign(file.id)
    return f"/api/download-file/{signed_value}/"
