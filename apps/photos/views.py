import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Photo
from .serializers import PhotoSerializer
from django.conf import settings
import os
from django_q.tasks import async_task
from django.core.cache import cache
from .tasks import process_user_photo_encodings
from .models import UserFaceEncoding
from rest_framework.permissions import AllowAny, IsAuthenticated

class PhotoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)

class PhotoDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            photo = Photo.objects.get(pk=pk)
            photo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Photo.DoesNotExist:
            return Response({"error": "Photo not found"}, status=status.HTTP_404_NOT_FOUND)

class UploadPhotoView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST.get('user_id')
        uploaded_file = request.FILES.get('file')

        if not uploaded_file or not user_id:
            return Response({"error": "user_id and file are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        upload_dir = settings.MEDIA_PATH
        os.makedirs(upload_dir, exist_ok=True)

        file_name = uploaded_file.name
        file_path = os.path.join(upload_dir, file_name)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        photo = Photo.objects.create(user_id=user_id, photo=file_name)
        serializer = PhotoSerializer(photo, context={'request': request})

        lock_key = f"user_encoding_processing_{user_id}"
        if not cache.get(lock_key):
            cache.set(lock_key, True, timeout=15)  # блокируем задачу на 15 секунд
            async_task('apps.photos.tasks.process_user_photo_encodings', user_id, schedule=time.time()+10)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GetAggregatedEncodingsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        encodings = {}
        try:
            records = UserFaceEncoding.objects.all()
            for record in records:
                encodings[str(record.user_id)] = record.encoding
            return Response(encodings, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)