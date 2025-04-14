from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Photo
from .serializers import PhotoSerializer
from django.conf import settings
import os

class PhotoView(APIView):
    def get(self, request):
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)

class PhotoDetailView(APIView):
    def delete(self, request, pk):
        try:
            photo = Photo.objects.get(pk=pk)
            photo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Photo.DoesNotExist:
            return Response({"error": "Photo not found"}, status=status.HTTP_404_NOT_FOUND)

class UploadPhotoView(APIView):

    def post(self, request):
        user_id = request.POST.get('user_id')
        uploaded_file = request.FILES.get('file')

        if not uploaded_file or not user_id:
            return Response({"error": "user_id and file are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем папку для пользователя
        folder_name = f"user_{user_id}"
        upload_dir = os.path.join("/usr/share/nginx/html", folder_name)  # путь на files.faceadmin.org
        os.makedirs(upload_dir, exist_ok=True)

        file_name = uploaded_file.name
        file_path = os.path.join(upload_dir, file_name)

        # Сохраняем файл
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Формируем URL и сохраняем в БД
        public_url = f"https://files.faceadmin.org/{folder_name}/{file_name}"
        photo = Photo.objects.create(user_id=user_id, photo=public_url)

        serializer = PhotoSerializer(photo, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
