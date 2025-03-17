from rest_framework import serializers
from .models import Log

class LogSerializer(serializers.ModelSerializer):
    user_fname = serializers.CharField(source="user.fname", read_only=True)
    user_lname = serializers.CharField(source="user.lname", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Log
        fields = ["id", "user", "user_fname", "user_lname", "user_email", "action", "timestamp"]
