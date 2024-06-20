from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import CustomUser, UploadedFile
from .serializers import CustomUserSerializer, UploadedFileSerializer
from django.core.signing import Signer

class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        verification_code = get_random_string(length=6)
        user.verification_code = verification_code
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

class LoginView(generics.GenericAPIView):
    pass
    # Implement login logic

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
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, file_id):
        file = UploadedFile.objects.get(id=file_id)
        if not request.user.is_client_user:
            raise PermissionDenied('Only client users can download files')
        download_link = generate_download_link(file)
        return Response({'download-link': download_link, 'message': 'success'})

def generate_download_link(file):
    signer = Signer()
    signed_value = signer.sign(file.id)
    return f"/api/download-file/{signed_value}/"
