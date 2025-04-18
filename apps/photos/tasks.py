import os
from django.conf import settings
from .models import Photo, UserFaceEncoding
import face_recognition
import numpy as np

def process_user_photo_encodings(user_id, **kwargs):
    photos = Photo.objects.filter(user_id=user_id)
    print(f"[DEBUG] Found {photos.count()} photos for user: {user_id}")
    all_encodings = []
    processed_files = 0

    for photo in photos:
        file_name = photo.photo
        file_path = os.path.join(settings.MEDIA_PATH, file_name)
        if os.path.exists(file_path):
            try:
                image = face_recognition.load_image_file(file_path)
                locations = face_recognition.face_locations(image)
                encodings = face_recognition.face_encodings(image, locations)
                if encodings:
                    all_encodings.append(encodings[0])
                    processed_files += 1
                    print(f"[DEBUG] Processed encoding from file: {file_name}")
                else:
                    print(f"[WARNING] Face not found in file: {file_name}")
            except Exception as e:
                print(f"[ERROR] Error processing file {file_name}: {str(e)}")
        else:
            print(f"[ERROR] File not found: {file_path}")

    if all_encodings:
        aggregated = np.mean(np.array(all_encodings), axis=0)
        aggregated_list = aggregated.tolist()
        face_record, created = UserFaceEncoding.objects.update_or_create(
            user_id=user_id,
            defaults={'encoding': aggregated_list}
        )
        message = f"Aggregated encoding processed for user: {user_id}. Based on {processed_files} photos out of {photos.count()} total."
    else:
        message = f"No valid encodings found for user: {user_id}"
    print(message)
    return message
