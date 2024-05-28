import face_recognition
import numpy as np
import os
from picamera2 import Picamera2
import paho.mqtt.client as mqtt
import ssl
import time
import json
from datetime import datetime

# Khởi tạo Picamera2
picam2 = Picamera2()
capture_config = picam2.create_still_configuration(main={"size": (320, 240)})
picam2.configure(capture_config)
picam2.start()

# Cấp phát bộ nhớ cho hình ảnh đầu ra
output = np.empty((240, 320, 3), dtype=np.uint8)

# Tải ảnh khuôn mặt đã biết
print("Thiết lập dữ liệu nhân viên...")
known_person = []
known_face_encoding = []

# Vòng lặp để thêm ảnh trong thư mục friends
for file in os.listdir("friends"):
    try:
        person_name = file.replace(".jpg", "")
        file_path = os.path.join("friends", file)
        known_image = face_recognition.load_image_file(file_path)
        known_face_encoding.append(face_recognition.face_encodings(known_image)[0])
        known_person.append(person_name)
    except Exception as e:
        print(f"Lỗi khi nhận diện nhân viên {file}: {e}")

# Cấu hình MQTT
broker_address = "4cc5961d8ff0416e9956c759300dd3ce.s1.eu.hivemq.cloud"
broker_port = 8883  # Cổng bảo mật cho MQTT qua TLS/SSL
topic = "Device"

# Các hàm callback của MQTT
def on_connect(client, userdata, flags, rc, properties=None):
    print("Đã kết nối với server " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

# Tạo MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set("vuduyphuong", "Phuong153280@")  # Thiết lập thông tin đăng nhập MQTT
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ca_certs=None)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port, 60)
client.loop_start()

try:
    while True:
        print("Đang chụp ảnh.")
        try:
            # Chụp ảnh vào mảng numpy
            capture = picam2.capture_array()
            output[:, :, :] = capture
            print("Chụp ảnh thành công")
        except Exception as e:
            print("Lỗi khi chụp ảnh:", e)
            continue

        # Tìm tất cả khuôn mặt và mã hóa khuôn mặt trong khung hình hiện tại
        face_locations = face_recognition.face_locations(output)
        print(f"Đã tìm thấy {len(face_locations)} khuôn mặt trong ảnh.")
        face_encodings = face_recognition.face_encodings(output, face_locations)

        # Vòng lặp qua từng khuôn mặt được tìm thấy trong khung để xem đó có phải là người chúng ta biết không
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
            if True in matches:
                first_match_index = matches.index(True)
                name = known_person[first_match_index]
            else:
                name = "A Stranger"

            print(f"{name} đang ở trong phòng !")
            
            # Lấy thời gian hiện tại
            detection_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Gửi tên người nhận diện được và thời gian đến máy chủ MQTT
            data = {
                "person": name,
                "time": detection_time
            }
            json_data = json.dumps(data)
            client.publish(topic, payload=json_data)
            print("Đã gửi dữ liệu cho server:", json_data)

        time.sleep(10)  # Điều chỉnh tần suất chụp ảnh

except KeyboardInterrupt:
    print("Đã ngắt kết nối!")

finally:
    client.loop_stop()
    client.disconnect()
    picam2.stop()
