import cv2 as cv
import base64
import pickle


def authenticate(staff_id, password):
    file = open('..\\db\\local_db.p', 'rb')
    students, staff = pickle.load(file)

    is_valid_cred = False
    data = {}
    for person in staff:
        if person['staff_id'] == staff_id and person['password'] == password:
            is_valid_cred = True
            data = person
            break

    return {
        'success': is_valid_cred,
        'data': data
    }


def get_student_data(index):
    file = open('..\\db\\local_db.p', 'rb')
    students, staff = pickle.load(file)
    file.close()

    student_data = {}
    for student in students:
        if int(student['index_no']) == int(index):
            student_data = student
            break

    # get the image and convert into base64
    image = cv.imread(f'images/{index}.jpg')
    base64_image = base64.b64encode(cv.imencode('.jpg', image)[1])
    student_data['image'] = base64_image

    return student_data


def enroll_student(image, name, index, programme):
    file_name = f'images/{index}.jpg'
    cv.imwrite(file_name, image)

    file = open('..\\db\\local_db.p', 'rb')
    students, staff = pickle.load(file)
    new_student = {
        'name': name,
        'index_no': index,
        'programme': programme
    }
    students.append(new_student)
    file = open('..\\db\\local_db.p', 'wb')
    pickle.dump([students, staff], file)
    file.close()
