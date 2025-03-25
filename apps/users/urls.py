from django.urls import path
from .views import LogoutView, MeView, UserView, LoginView, VerifyOTPView

urlpatterns = [
    path('', UserView.as_view()),
    path('<int:pk>/', UserView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('me/', MeView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
]
