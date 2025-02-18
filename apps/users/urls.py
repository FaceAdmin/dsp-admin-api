from django.urls import path

from .views import UserView, LoginView, PhotoView

urlpatterns = [
    path('', UserView.as_view()),           # GET all users or POST create user
    path('<int:pk>/', UserView.as_view()),  # GET/DELETE/PATCH user by ID
    path('login/', LoginView.as_view()),    # POST for login
    path('', PhotoView.as_view()),          # GET all photos or POST create
    path('<int:pk>/', PhotoView.as_view()), # GET photo by ID
]
