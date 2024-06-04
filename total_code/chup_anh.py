import cv2
from picamera2 import Picamera2
import time

# Khởi tạo camera
picam2 = Picamera2()
max_resolution = picam2.sensor_resolution  
picam2.preview_configuration.main.size = max_resolution
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

cpt = 0

while True:
    im = picam2.capture_array()
    cv2.imshow("Camera", im)

    if cv2.waitKey(1) == ord('q'):
        # Khi nhấn phím 'q', chụp và lưu ảnh
        cv2.imwrite(f'/home/edabk/image/fan-light{cpt}.jpg', im)
        print(f"Image {cpt} captured and saved.")
        cpt += 1

    if cv2.waitKey(1) == 27:  # ESC key to exit
        break

cv2.destroyAllWindows()
picam2.stop()
