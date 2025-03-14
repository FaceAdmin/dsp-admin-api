from django.urls import path
from .views import PhotoView

urlpatterns = [
    path('', PhotoView.as_view()),
]
