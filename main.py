from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import face_recognition
import cv2 as cv
import numpy as np
import base64
import pickle
from database import get_student_data, enroll_student

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

file = open('db\\encodings.p', 'rb')
encoded_images_database, labels_database = pickle.load(file)
file.close()

print('labels_database', labels_database)


def base64_to_image(base64_image):
    try:
        # decode base64 to bytes
        image_bytes = base64.b64decode(base64_image)
        # decode bytes to numpy array
        np_array = np.frombuffer(image_bytes, dtype='uint8')
        # decode numpy array as an image
        image = cv.imdecode(np_array, cv.IMREAD_COLOR)
        return image
    except Exception as e:
        print(e)


def determine_face_match(image):
    try:
        resized_image = cv.resize(image, (0, 0), None, 0.25, 0.25)
        rgb_image = cv.cvtColor(resized_image, cv.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_image)
        encoded_faces = face_recognition.face_encodings(rgb_image, face_locations)

        match_labels = []
        for encoded_face in encoded_faces:
            match_bool_list = face_recognition.compare_faces(encoded_images_database, encoded_face)
            match_face_distances_list = face_recognition.face_distance(encoded_images_database, encoded_face)
            # get index of smallest distance
            match_index = np.argmin(match_face_distances_list)
            # confirm that the match index is also true for the compared faces
            if match_bool_list[match_index]:
                match_labels.append(labels_database[match_index])

        return match_labels

    except Exception as e:
        print(e)


def encode_image(image, label):
    face_locations = face_recognition.face_locations(image)
    img_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    encoding = face_recognition.face_encodings(img_rgb, face_locations)[0]

    encoded_images_database.append(encoding)
    labels_database.append(label)

    file2 = open('db\\encodings.p', 'wb')
    pickle.dump([encoded_images_database, labels_database], file2)
    file2.close()

    y1, x2, y2, x1 = face_locations[0]
    cropped_img = image[y1 - 60:y2 + 30, x1 - 30:x2 + 30]

    return cropped_img


@app.post('/login')
async def login(req: Request):
    staff_id, password = await req.json()


# get base64 image and compare to encodings
@app.post('/image')
async def recognizer(req: Request):
    print('processing...')
    base64_image = await req.json()
    # convert base64 to an image
    image = base64_to_image(base64_image['base64_image'])
    labels = determine_face_match(image)
    print(labels)

    if len(labels) == 0:
        return {}
    else:
        return get_student_data(labels[0])

    # resized_image = cv.resize(image, (0, 0), None, 0.25, 0.25)
    # cv.imshow('Works!', resized_image)
    # cv.waitKey(0)


# test feature: for enrolling new students
@app.post('/enroll')
async def enroll_student_test(req: Request):
    print('enrolling...')
    enrollment_data = await req.json()
    base64_image = enrollment_data['base64_image']
    name = enrollment_data['name']
    index = enrollment_data['index']
    programme = enrollment_data['programme']

    image = base64_to_image(base64_image)
    cropped_image = encode_image(image, index)
    enroll_student(cropped_image, name, index, programme)

    return {}
