import pickle
import face_recognition
import cv2 as cv

students = [
    {
        'name': 'Jerome Akumasi',
        'index_no': '8251723',
        'programme': 'Bsc. Computer Engineering'
    }
]

staff = [
    {
        'name': 'Prof. A1',
        'staff_id': '8822110',
        'password': '123456'
    }
]

local_db = [students, staff]
file = open('db/local_db.p', 'wb')
pickle.dump(local_db, file)
file.close()

path = 'C:\\users\\jerome akumasi\\desktop\\8251723.jpg'
image = cv.imread(path)

face_locations = face_recognition.face_locations(image)
img_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
encoding = face_recognition.face_encodings(img_rgb, face_locations)[0]
file = open('db/encodings.p', 'wb')
pickle.dump([[encoding], ['8251723']], file)
file.close()

y1, x2, y2, x1 = face_locations[0]
cropped_img = image[y1 - 60:y2 + 30, x1 - 30:x2 + 30]
cv.imwrite('images/8251723.jpg', cropped_img)


# file = open('encoded.p', 'rb')
# encodings, labels = pickle.load(file)
# print(labels)


# file = open('local_db.p', 'wb')
# students, staff = pickle.load(file)
# file.close()
