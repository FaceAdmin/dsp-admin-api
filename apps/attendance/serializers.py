from rest_framework import serializers
from apps.attendance.models import Attendance
from apps.users.models import User

class AttendanceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    check_in = serializers.DateTimeField(required=False, allow_null=True)
    check_out = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Attendance
        fields = (
            'attendance_id',
            'user',
            'check_in',
            'check_out',
            'duration',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['user'] = {
            "user_id": instance.user.user_id,
            "fname": instance.user.fname,
            "lname": instance.user.lname,
            "email": instance.user.email,
            "role": instance.user.role,
        }
        return ret

    def get_user(self, obj):
        return {
            "user_id": obj.user.user_id,
            "fname": obj.user.fname,
            "lname": obj.user.lname,
            "email": obj.user.email,
            "role": obj.user.role,
        }

    def get_check_in(self, obj):
        if obj.check_in:
            return obj.check_in.isoformat()
        return None

    def get_check_out(self, obj):
        if obj.check_out:
            return obj.check_out.isoformat()
        return None
    
    def update(self, instance, validated_data):
        instance.check_in = validated_data.get('check_in', instance.check_in)
        instance.check_out = validated_data.get('check_out', instance.check_out)

        if instance.check_in and instance.check_out:
            delta = instance.check_out - instance.check_in
            instance.duration = delta
        else:
            instance.duration = None

        instance.save()
        return instance
