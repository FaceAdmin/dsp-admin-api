# Generated by Django 4.2.6 on 2025-03-27 15:47

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_otp_configured_user_otp_secret'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='otp_secret',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=32, null=True)),
        ),
    ]
