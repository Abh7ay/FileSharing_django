from django.urls import path
from .views import UserSignUpView, LoginView, FileUploadView, FileListView, FileDownloadView

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', FileListView.as_view(), name='file-list'),
    path('download/<int:file_id>/', FileDownloadView.as_view(), name='file-download'),
]
