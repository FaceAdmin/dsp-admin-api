from django.urls import path
from .views import generate_csv_report

urlpatterns = [
    path('csv/', generate_csv_report, name='generate_csv_report'),
]
