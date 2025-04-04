from django.urls import path
from .views import LogoutView, MeView, RegenerateOTPSecretView, ResendOTPEmailView, UserView, LoginView, VerifyOTPView

urlpatterns = [
    path('', UserView.as_view()),
    path('<int:pk>/', UserView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('me/', MeView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPEmailView.as_view(), name='resend-otp'),
    path('<int:pk>/regenerate-otp/', RegenerateOTPSecretView.as_view()),
]
