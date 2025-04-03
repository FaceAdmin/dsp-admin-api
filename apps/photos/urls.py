from django.urls import path
from .views import PhotoView, PhotoDetailView, UploadPhotoView

urlpatterns = [
    path('', PhotoView.as_view()),
    path('<int:pk>/', PhotoDetailView.as_view()),
    path('upload/', UploadPhotoView.as_view()),
]
