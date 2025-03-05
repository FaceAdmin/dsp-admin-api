from django.urls import path
from .views import AttendanceView

urlpatterns = [
    path('', AttendanceView.as_view()),
    path('<int:pk>/', AttendanceView.as_view())
]
