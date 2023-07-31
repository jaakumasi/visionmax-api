import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, storage
import cv2 as cv
import base64
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

# data = {
#     'name': "Prof. A1", 'password': "221133"
# }
# db.reference('staff').child('8060709').set(data)


def get_student_data(index):
    student_data = db.reference(f'students/{index}').get()
    bucket = storage.bucket()
    blob = bucket.get_blob(f'images/{index}.jpg')
    base64_image = base64.b64encode(blob.download_as_string())

    student_data['image'] = base64_image

    return student_data


def enroll_student(cropped_image, name, index, programme):
    file_name = f'images/{index}.jpg'
    cv.imwrite(file_name, cropped_image)

    # save image to storage bucket
    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)

    # save data to database
    ref = db.reference('students')
    data = {
        'name': name,
        'index_no': index,
        'programme': programme
    }
    ref.child(index).set(data)
