import face_recognition as fr
from employee.models import Employee
import numpy as np


def is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def get_encoded_faces():
    """
    Hàm này lấy tất cả ảnh các nhân viên và mã hoá khuôn mặt họ
    """
    # Lấy toàn bộ thông tin nhân viên từ database
    qs = Employee.objects.all()

    # Tạo biến để lưu trữ ảnh mã hóa của từng nhân viên
    encoded = {}

    for p in qs:
        # Khởi tạo biến encoding với giá trị None
        encoding = None

        # Tải ảnh của nhân viên lên
        face = fr.load_image_file(p.photo.path)

        # Mã hoá khuôn mặt của nhân viên
        face_encodings = fr.face_encodings(face)
        if len(face_encodings) > 0:
            encoding = face_encodings[0]
        else:
            print("No face found in the image")

        # Thêm mã hoá khuôn mặt của nhân viên vào biến từ điển encoded nếu encoding khác None
        if encoding is not None:
            encoded[p.user.username] = encoding

    return encoded


def classify_face(img):
    """
    Hàm này có chức năng nhận diện khuôn mặt trong ảnh và trả về tên của người đó
    """
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = fr.load_image_file(img)

    try:
        face_locations = fr.face_locations(img)

        unknown_face_encodings = fr.face_encodings(img, face_locations)

        face_names = []
        for face_encoding in unknown_face_encodings:
            matches = fr.compare_faces(faces_encoded, face_encoding)

            face_distances = fr.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            else:
                name = "Unknown"

            face_names.append(name)

        return face_names[0]
    except:
        print("Cannot classify face")
        return False
