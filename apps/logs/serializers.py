from rest_framework import serializers
from .models import Log

class LogSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    user_last_name = serializers.CharField(source="user.last_name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Log
        fields = ["id", "user", "user_first_name", "user_last_name", "user_email", "action", "timestamp"]
