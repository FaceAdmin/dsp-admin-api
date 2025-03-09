from django.urls import path

from .views import LogoutView, MeView, UserView, LoginView, PhotoView

urlpatterns = [
    path('', UserView.as_view()),
    path('<int:pk>/', UserView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('me/', MeView.as_view()),

    path('', PhotoView.as_view()),
    path('<int:pk>/', PhotoView.as_view()),
]
