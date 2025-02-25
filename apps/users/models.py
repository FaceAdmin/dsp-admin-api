from django.db import models
from django.contrib.auth.hashers import make_password, is_password_usable

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        db_column='user_id'
    )
    photo_path = models.TextField()

    class Meta:
        db_table = 'photos'