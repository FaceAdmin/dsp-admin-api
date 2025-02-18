from django.db import models
from apps.users.models import User

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True,)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user_id'
    )
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    class Meta:
        db_table = 'attendance'