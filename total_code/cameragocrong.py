import cv2
from picamera2 import Picamera2
import time

picam2 = Picamera2()
max_resolution = picam2.sensor_resolution  # Lấy độ phân giải tối đa của cảm biến
picam2.preview_configuration.main.size = max_resolution
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

cpt = 0
maxFrames = 1000  # Giới hạn số lượng ảnh để chụp

while True:
    im = picam2.capture_array()
    cv2.imshow("Camera", im)
    cv2.imwrite(f'/home/edabk/image/fan-light{cpt}.jpg', im)
    cpt += 1
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
