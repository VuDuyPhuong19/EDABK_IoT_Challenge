import cv2
#from picamera2 import Picamera2
import time
import json
from roboflow import Roboflow
import os
from PIL import Image

def convert_predictions_to_custom_format_small(input_json_path, output_json_path):
 
    with open(input_json_path, 'r') as input_file:
        prediction_results = json.load(input_file)

    rois = []
    labels = []

    for prediction in prediction_results['predictions']:
        obj_class = prediction['class']
        x = prediction['x']
        y = prediction['y']
        width = prediction['width']
        height = prediction['height']
        
        xmin = int(x - width / 2)
        ymin = int(y - height / 2)
        xmax = int(x + width / 2)
        ymax = int(y + height / 2)

        rois.append([xmin, ymin, xmax - xmin, ymax - ymin])
        labels.append(obj_class)

    custom_format = {"rois": rois, "labels": labels}

    with open(output_json_path, 'w') as output_file:
        json.dump(custom_format, output_file, indent=4)

    print(f"Saved converted results to {output_json_path}")
def convert_predictions_to_custom_format_big(input_json_path, output_json_path, old_size=(1080, 608), new_size=(4608, 2592)):
    with open(input_json_path, 'r') as input_file:
        prediction_results = json.load(input_file)

    rois = []
    labels = []

    old_width, old_height = old_size
    new_width, new_height = new_size

    for prediction in prediction_results['predictions']:
        obj_class = prediction['class']
        x = prediction['x']
        y = prediction['y']
        width = prediction['width']
        height = prediction['height']
        
        
        x_new = x * new_width / old_width
        y_new = y * new_height / old_height
        width_new = width * new_width / old_width
        height_new = height * new_height / old_height
        
        xmin = int(x_new - width_new / 2)
        ymin = int(y_new - height_new / 2)
        xmax = int(x_new + width_new / 2)
        ymax = int(y_new + height_new / 2)

        rois.append([xmin, ymin, xmax - xmin, ymax - ymin])
        labels.append(obj_class)

    custom_format = {"rois": rois, "labels": labels}

    with open(output_json_path, 'w') as output_file:
        json.dump(custom_format, output_file, indent=4)

    print(f"Saved converted results to {output_json_path}")
    
def convert_rois_to_custom_format_giantiep(input_json_path, output_json_path, old_size=(1080, 608), new_size=(4608, 2592)):
    try:
        with open(input_json_path, 'r') as input_file:
            data = json.load(input_file)

        rois = data.get('rois', [])
        labels = data.get('labels', [])

        old_width, old_height = old_size
        new_width, new_height = new_size

        new_rois = []

        for roi in rois:
            xmin, ymin, width, height = roi
            
           
            x_new = xmin * new_width / old_width
            y_new = ymin * new_height / old_height
            width_new = width * new_width / old_width
            height_new = height * new_height / old_height

            new_rois.append([int(x_new), int(y_new), int(width_new), int(height_new)])

        custom_format = {"rois": new_rois, "labels": labels}

        with open(output_json_path, 'w') as output_file:
            json.dump(custom_format, output_file, indent=4)

        print(f"Saved converted results to {output_json_path}")

    except Exception as e:
        print(f"An error occurred: {e}")    
def compress_image(image_path, max_size=(1080, 720), quality=75):
  
    # Open and compress the image
    with Image.open(image_path) as img:
        img.thumbnail(max_size, Image.LANCZOS)
        img.save(image_path, 'JPEG', quality=quality, optimize=True)
        
    print(f"Compressed image saved at {image_path}")


# Initialize Picamera2
#picam2 = Picamera2()
#max_resolution = picam2.sensor_resolution  
#picam2.preview_configuration.main.size = max_resolution
#picam2.preview_configuration.main.size = (640, 480)
#picam2.preview_configuration.main.format = "RGB888"
#picam2.preview_configuration.align()
#picam2.configure("preview")
#picam2.start()

# Initialize Roboflow
rf = Roboflow(api_key="jRJfDI9kcN7jQh83c9tj")
project = rf.workspace().project("light_fan")
model = project.version("4").model

# Capture image from camera
#image = picam2.capture_array()
#cv2.imwrite('/home/edabk/image_detect_roboflow/image.jpg', image)
#print("Image captured and saved.")

# Close camera preview
#cv2.destroyAllWindows()
#picam2.stop()

image_path = "/home/edabk/image_detect_roboflow/image.jpg"

compress_image(image_path)
# Predict using Roboflow
prediction_results = model.predict(image_path, confidence=40, overlap=30).json()

predicted_image_path = image_path.replace(".jpg", "-prediction.jpg")

model.predict(image_path, confidence=40, overlap=30).save(predicted_image_path)

# Save prediction results to JSON
json_file_path = image_path.replace(".jpg", ".json")
with open(json_file_path, 'w') as json_file:
    json.dump(prediction_results, json_file, indent=4)

print("Saved predicted image and JSON results.")

# Print prediction results
for prediction in prediction_results['predictions']:
    obj_class = prediction['class']
    x = prediction['x']
    y = prediction['y']
    width = prediction['width']
    height = prediction['height']
    confidence = prediction['confidence']
    print(f"Class: {obj_class}, X: {x}, Y: {y}, Width: {width}, Height: {height}, Confidence: {confidence:.2f}")

input_json_path = '/home/edabk/image_detect_roboflow/image.json'
output_json_path = '/home/edabk/image_detect_roboflow/image_convert.json'
convert_predictions_to_custom_format_small(input_json_path, output_json_path)

input_json_path2 = '/home/edabk/image_detect_roboflow/image_convert.json'    
output_json_path2 = '/home/edabk/image_detect_roboflow/image_convert4608.json'
# Example usage
convert_rois_to_custom_format_giantiep(input_json_path2, output_json_path2)