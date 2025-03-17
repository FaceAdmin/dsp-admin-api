from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.attendance.models import Attendance
from apps.attendance.serializers import AttendanceSerializer

class AttendanceView(APIView):
    def get(self, request, pk=None):
        user_id = request.query_params.get('user_id')
        date_param = request.query_params.get('date')

        if user_id:
            records = Attendance.objects.filter(user__user_id=user_id)
            if date_param:
                records = records.filter(check_in__date=date_param)
            serializer = AttendanceSerializer(records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if pk:
            try:
                attendance = Attendance.objects.get(pk=pk)
            except Attendance.DoesNotExist:
                return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if date_param:
            records = Attendance.objects.filter(check_in__date=date_param)
        else:
            records = Attendance.objects.all()

        serializer = AttendanceSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            record = Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AttendanceSerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            record = Attendance.objects.get(pk=pk)
            record.delete()
            return Response({"message": "Attendance record deleted successfully"}, status=status.HTTP_200_OK)
        except Attendance.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
