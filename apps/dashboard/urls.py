from django.urls import path
from .views import DashboardDataView

urlpatterns = [
    path('data/', DashboardDataView.as_view(), name='dashboard_data'),
]
