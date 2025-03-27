from django.db import models
from django_cryptography.fields import encrypt

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    otp_secret = encrypt(models.CharField(max_length=32, blank=True, null=True))
    otp_configured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'