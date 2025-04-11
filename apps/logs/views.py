from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Log
from .serializers import LogSerializer

class LogView(APIView):
    def get(self, request):
        logs = Log.objects.order_by("-timestamp")[:50]
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LogSerializer(data=request.data)
        if serializer.is_valid():
            log = serializer.save()
            total_logs = Log.objects.count()
            if total_logs > 1000:
                overflow = total_logs - 1000
                oldest_logs = Log.objects.order_by("timestamp")[:overflow]
                Log.objects.filter(pk__in=[log.pk for log in oldest_logs]).delete()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
