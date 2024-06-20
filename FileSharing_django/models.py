from django.db import models

class User(models.Model):
    operation_user = models.BooleanField(default=False)
    client_user = models.BooleanField(default=False)

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
 