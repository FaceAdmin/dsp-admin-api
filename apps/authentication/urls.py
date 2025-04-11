from django.urls import path
from .views import auth_check, login_view, logout_view

urlpatterns = [
    path('', auth_check, name='auth_check'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
