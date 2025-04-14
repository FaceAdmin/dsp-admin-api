from django.db import models
from apps.users.models import User

def user_directory_path(instance, filename):
    return f"user_{instance.user.user_id}/{filename}"

class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user_id'
    )
    photo = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    class Meta:
        db_table = 'photos'

    def delete(self, *args, **kwargs):
        self.photo.delete(save=False)
        super().delete(*args, **kwargs)
