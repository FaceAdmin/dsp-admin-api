from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.attendance.models import Attendance
from apps.attendance.serializers import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated

class AttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user       = request.user
        date_param = request.query_params.get("date")
        user_id    = request.query_params.get("user_id")

        if user.role != "Admin":
            if pk:
                attendance = get_object_or_404(Attendance, pk=pk, user=user)
                serializer = AttendanceSerializer(attendance)
                return Response(serializer.data, status=status.HTTP_200_OK)

            queryset = Attendance.objects.filter(user=user)
            if date_param:
                queryset = queryset.filter(check_in__date=date_param)

            serializer = AttendanceSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if pk:
            attendance = get_object_or_404(Attendance, pk=pk)
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        queryset = Attendance.objects.all()
        if user_id:
            queryset = queryset.filter(user_id=user_id, check_out__isnull=True)
        if date_param:
            queryset = queryset.filter(check_in__date=date_param)

        serializer = AttendanceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        record = get_object_or_404(Attendance, pk=pk)
        serializer = AttendanceSerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        record = get_object_or_404(Attendance, pk=pk)
        record.delete()
        return Response({"message": "Attendance record deleted successfully"}, status=status.HTTP_200_OK)
