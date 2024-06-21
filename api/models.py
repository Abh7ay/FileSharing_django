from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_ops_user = models.BooleanField(default=False)
    is_client_user = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=100, null=True, blank=True)

class UploadedFile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=5, choices=[('pptx', 'PPTX'), ('docx', 'DOCX'), ('xlsx', 'XLSX')])
