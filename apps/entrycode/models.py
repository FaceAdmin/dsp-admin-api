from django.db import models
from apps.users.models import User

class EntryCode(models.Model):
    code_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name="entry_code"
    )
    code = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'entry_codes'
    
    def __str__(self):
        return f"{self.user.fname} {self.user.lname} - {self.code}"
