from face_recognition import face_encodings
import cv2 as cv
import pickle
import os
import numpy as np
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import os
from dotenv import load_dotenv

load_dotenv()

service_account_key = {
    'type': os.environ.get('FIREBASE_TYPE'),
    'project_id': os.environ.get('FIREBASE_PROJECT_ID'),
    'private_key_id': os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
    'private_key': os.environ.get('FIREBASE_PRIVATE_KEY').encode().decode('unicode_escape'),
    'client_email': os.environ.get('FIREBASE_CLIENT_EMAIL'),
    'client_id': os.environ.get('FIREBASE_CLIENT_ID'),
    'auth_uri': os.environ.get('FIREBASE_AUTH_URI'),
    'token_uri': os.environ.get('FIREBASE_TOKEN_URI'),
    'auth_provider_x509_cert_url': os.environ.get('FIREBASE_AUTH_PROVIDER_CERT_URL'),
    'client_x509_cert_url': os.environ.get('FIREBASE_CLIENT_CERT_URL'),
    'universe_domain': os.environ.get('FIREBASE_UNIVERSE_DOMAIN')
}

cred = credentials.Certificate(service_account_key)
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://real-time-database-9c898-default-rtdb.firebaseio.com/",
    'storageBucket': 'real-time-database-9c898.appspot.com'
})

imagesPath = '.\\images'
images = []
labels = []

for img in os.listdir(imagesPath):
    images.append(cv.imread(os.path.join(imagesPath, img)))
    labels.append(os.path.splitext(img)[0])


def encode_images(image_list):
    encoded_img_list = []

    for idx, img in enumerate(image_list):
        try:
            face_locations = face_recognition.face_locations(img)
            img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            encoding = face_recognition.face_encodings(img_rgb, face_locations)[0]
            encoded_img_list.append(encoding)

            # y1, x2, y2, x1 = face_locations[0]
            # cropped_img = img[y1 - 60:y2 + 30, x1 - 30:x2 + 30]
            # file_name = f'images/{labels[idx]}.jpg'
            # cv.imwrite(file_name, cropped_img)
            #
            #
            # bucket = storage.bucket()
            # blob = bucket.blob(file_name)
            # blob.upload_from_filename(file_name)


        except Exception as e:
            print(e)

    return encoded_img_list

print(labels)

encoded_images = encode_images(images)
# save image encodings with their corresponding labels into an array
encoded_images_with_ids = [encoded_images, labels]

file = open('encoded.p', 'ab+')
pickle.dump(encoded_images_with_ids, file)
file.close()