import os
from django.conf import settings
from .models import Photo, UserFaceEncoding
import face_recognition
import numpy as np

def process_user_photo_encodings(user_id):
    """
    Обрабатываем все фотографии пользователя: для каждого фото вычисляем индивидуальный face encoding,
    затем агрегируем (среднее) все векторы и сохраняем результат в модели UserFaceEncoding.
    Если для пользователя уже существует запись, она обновляется.
    """
    photos = Photo.objects.filter(user_id=user_id)
    all_encodings = []
    for photo in photos:
        file_name = photo.photo
        file_path = os.path.join(settings.MEDIA_PATH, file_name)
        if os.path.exists(file_path):
            try:
                image = face_recognition.load_image_file(file_path)
                locations = face_recognition.face_locations(image)
                encodings = face_recognition.face_encodings(image, locations)
                if encodings:
                    # Используем первый вычисленный вектор для фото
                    all_encodings.append(encodings[0])
                else:
                    print(f"[WARNING] Лицо не найдено в файле: {file_name}")
            except Exception as e:
                print(f"[ERROR] Ошибка при обработке файла {file_name}: {str(e)}")
        else:
            print(f"[ERROR] Файл не найден: {file_path}")

    if all_encodings:
        aggregated = np.mean(np.array(all_encodings), axis=0)
        aggregated_list = aggregated.tolist()

        # Сохраняем или обновляем агрегированный encoding для пользователя
        face_record, created = UserFaceEncoding.objects.update_or_create(
            user_id=user_id,
            defaults={'encoding': aggregated_list}
        )
        message = f"Aggregated encoding processed for user: {user_id}"
    else:
        message = f"No valid encodings found for user: {user_id}"

    print(message)
    return message
