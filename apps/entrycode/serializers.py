from rest_framework import serializers
from apps.entrycode.models import EntryCode

class EntryCodeSerializer(serializers.ModelSerializer):
    user_fname = serializers.CharField(source="user.fname", read_only=True)
    user_lname = serializers.CharField(source="user.lname", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    
    class Meta:
        model = EntryCode
        fields = [
            'code_id',
            'user',
            'user_fname',
            'user_lname',
            'user_email',
            'code',
            'created_at',
            'updated_at',
        ]
