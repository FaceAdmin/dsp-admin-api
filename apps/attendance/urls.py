from django.urls import path
from .views import AttendanceView

urlpatterns = [
    path('', AttendanceView.as_view()),         # GET all attendance or POST create
    path('<int:pk>/', AttendanceView.as_view()) # GET/PATCH attendance by ID
]
