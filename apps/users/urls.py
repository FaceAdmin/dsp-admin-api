from django.urls import path
from .views import RegenerateOTPSecretView, ResendOTPEmailView, UserView, VerifyOTPView

urlpatterns = [
    path('', UserView.as_view()),
    path('<int:pk>/', UserView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPEmailView.as_view(), name='resend-otp'),
    path('<int:pk>/regenerate-otp/', RegenerateOTPSecretView.as_view()),
]
