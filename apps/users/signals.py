import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.users.models import User
from apps.entrycode.models import EntryCode

def generate_unique_code():
    while True:
        code = str(random.randint(10000000, 99999999))
        if not EntryCode.objects.filter(code=code).exists():
            return code

@receiver(post_save, sender=User)
def create_entry_code(sender, instance, created, **kwargs):
    if created:
        EntryCode.objects.create(user=instance, code=generate_unique_code())
