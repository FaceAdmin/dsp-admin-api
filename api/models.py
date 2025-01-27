from django.db import models
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk or 'password' in kwargs.get('update_fields', []):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

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

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True,)
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        db_column='user_id'
    )
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    class Meta:
        db_table = 'attendance'

