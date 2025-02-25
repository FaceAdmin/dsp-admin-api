from rest_framework import serializers
from .models import User, Photo
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    newPassword = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['user_id', 'fname', 'lname', 'email', 'role', 'password', 'newPassword', 'created_at', 'updated_at']
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


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'