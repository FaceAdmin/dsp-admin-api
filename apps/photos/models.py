from django.db import models
from apps.users.models import User

class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_column='user_id'
    )
    photo_path = models.TextField()

    class Meta:
        db_table = 'photos'
