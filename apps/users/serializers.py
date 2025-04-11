from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    newPassword = serializers.CharField(write_only=True, required=False)
    otp_configured = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'email', 'role',
            'password', 'newPassword', 'otp_configured', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        newPassword = validated_data.pop('newPassword', None)
        if newPassword:
            instance.password = make_password(newPassword)
        return super().update(instance, validated_data)
