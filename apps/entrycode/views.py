from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.entrycode.models import EntryCode
from apps.entrycode.serializers import EntryCodeSerializer

class EntryCodeView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                entry_code = EntryCode.objects.get(user__user_id=pk)  # <-- Ищем по user_id
            except EntryCode.DoesNotExist:
                return Response({"error": "Entry code not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = EntryCodeSerializer(entry_code)
            return Response(serializer.data)
        else:
            entry_codes = EntryCode.objects.all()
            serializer = EntryCodeSerializer(entry_codes, many=True)
            return Response(serializer.data)
    
    def post(self, request):
        serializer = EntryCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        try:
            entry_code = EntryCode.objects.get(pk=pk)
        except EntryCode.DoesNotExist:
            return Response({"error": "Entry code not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EntryCodeSerializer(entry_code, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            entry_code = EntryCode.objects.get(pk=pk)
            entry_code.delete()
            return Response({"message": "Entry code deleted successfully"}, status=status.HTTP_200_OK)
        except EntryCode.DoesNotExist:
            return Response({"error": "Entry code not found"}, status=status.HTTP_404_NOT_FOUND)
