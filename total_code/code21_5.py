

import cv2
import numpy as np
import json
from picamera2 import Picamera2
import paho.mqtt.client as mqtt
import ssl
import time

rois = []
labels = []
backSubs = []

# MQTT setup
broker_address = "b509faa6e72f4505a1a3885d80218fe7.s1.eu.hivemq.cloud"
broker_port = 8883  # Secure port for MQTT over TLS/SSL
topic = "App"

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))

# Camera setup
piCam = Picamera2()
max_resolution = piCam.sensor_resolution
preview_config = piCam.create_preview_configuration(main={"size": max_resolution, "format": "RGB888"})
piCam.configure(preview_config)
piCam.start()

def save_rois(filename="rois.json"):
    data = {'rois': rois, 'labels': labels}
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_rois(filename="2.json"):
    with open(filename, 'r') as f:
        data = json.load(f)
    rois[:] = data['rois']
    labels[:] = data['labels']
    backSubs[:] = [cv2.createBackgroundSubtractorMOG2() for _ in rois]

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, img
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 5)
            cv2.imshow('image', img_copy)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 5)
        roi = (ix, iy, x - ix, y - iy)
        label = input("Enter the label for this ROI (light/fan): ")
        rois.append(roi)
        labels.append(label)
        backSubs.append(cv2.createBackgroundSubtractorMOG2())
        save_rois()

def process_frame(frame):
    light_count = 0
    fan_count = 0
    fan_motion = 0
    for roi, label, backSub in zip(rois, labels, backSubs):
        x, y, w, h = roi
        roi_frame = frame[y:y+h, x:x+w]
        hsv = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)
        if label == 'light':
            mask = cv2.inRange(hsv, np.array([0, 0, 150]), np.array([0, 50, 255]))
            if cv2.countNonZero(mask) > 30:
                light_count += 1
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)
                cv2.putText(frame, 'Light ON', (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif label == 'fan':
            fgMask = backSub.apply(roi_frame)
            contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) > 100:
                    fan_motion += 1
                    x1, y1, w1, h1 = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x + x1, y + y1), (x + x1 + w1, y + y1 + h1), (255, 0, 0), 5)
                    cv2.putText(frame, 'Fan ON', (x + x1, y + y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            if fan_motion > 0:
                fan_count += 1
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Send the counts over MQTT
    data = {
        "light_on": light_count,
        "fan_on": fan_count,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    json_data = json.dumps(data)
    client.publish(topic, payload=json_data)
    print("Sent JSON data:", json_data)

    return frame

if input("Do you want to load previous ROIs? (yes/no): ").lower() == 'yes':
    load_rois()
else:
    img = piCam.capture_array()
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', draw_rectangle)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set("thanhdoo28803", "123456and7")  # Set your username and password
client.connect(broker_address, broker_port, 60)
client.loop_start()

cv2.namedWindow('Processed Frame', cv2.WINDOW_NORMAL)
try:
    while True:
        frame = piCam.capture_array()
        processed_frame = process_frame(frame)
        cv2.imshow('Processed Frame', processed_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    piCam.stop()
    cv2.destroyAllWindows()

