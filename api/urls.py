from django.urls import path
from .views import SignUpView, VerifyEmailView, LoginView, UploadFileView, ListFilesView, DownloadFileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload-file/', UploadFileView.as_view(), name='upload-file'),
    path('list-files/', ListFilesView.as_view(), name='list-files'),
    path('download-file/<int:file_id>/', DownloadFileView.as_view(), name='download-file'),
]
