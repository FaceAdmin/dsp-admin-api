from django.urls import path
from .views import EntryCodeView

urlpatterns = [
    path('', EntryCodeView.as_view()),
    path('<int:pk>/', EntryCodeView.as_view()),
]
