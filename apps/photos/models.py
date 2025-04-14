import os
from django.db import models
from apps.users.models import User
from faceadmin import settings

def user_directory_path(instance, filename):
    return f"user_{instance.user.user_id}/{filename}"

class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user_id'
    )
    photo = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'photos'

    def delete(self, *args, **kwargs):
        file_path = os.path.join(settings.MEDIA_PATH, self.photo)
        if os.path.exists(file_path):
            os.remove(file_path)
        super().delete(*args, **kwargs)

class UserFaceEncoding(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='face_encoding'
    )
    encoding = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'user_face_encoding'