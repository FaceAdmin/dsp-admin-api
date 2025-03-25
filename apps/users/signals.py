import pyotp
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.users.models import User
from apps.users.utils import send_otp_email

@receiver(post_save, sender=User)
def generate_otp_secret(sender, instance, created, **kwargs):
    if created:
        if not instance.otp_secret:
            instance.otp_secret = pyotp.random_base32()
            instance.otp_configured = False
            instance.save()
            send_otp_email(instance)
