from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)

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

