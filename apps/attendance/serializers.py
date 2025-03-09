from rest_framework import serializers
from apps.attendance.models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    check_in = serializers.SerializerMethodField()
    check_out = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = (
            'attendance_id',
            'user',
            'check_in',
            'check_out',
            'duration',
        )

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
