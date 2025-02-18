from rest_framework import serializers
from .models import User, Photo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'fname', 'lname', 'email', 'role', 'password', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True},
        }

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'