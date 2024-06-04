import numpy as np
import os
from tflite_model_maker.config import ExportFormat, QuantizationConfig
from tflite_model_maker import model_spec
from tflite_model_maker import object_detector
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow as tf

assert tf.__version__.startswith('2')

tf.get_logger().setLevel('ERROR')
from absl import logging
logging.set_verbosity(logging.ERROR)

# Load training and validation data
train_data = object_detector.DataLoader.from_pascal_voc(
    'image_train_colab/train',
    'image_train_colab/train',
    ['light', 'fan']
)

val_data = object_detector.DataLoader.from_pascal_voc(
    'image_train_colab/valid',
    'image_train_colab/valid',
    ['light', 'fan']
)

# Define model specification
spec = model_spec.get('efficientdet_lite0')

# Path to save/load model weights
weights_path = '/content/gdrive/MyDrive/train_detect_object/model_weights.h5'

# Create and train the model
model = object_detector.create(
    train_data, 
    model_spec=spec, 
    batch_size=16, 
    train_whole_model=True, 
    epochs=1,  # Initial epochs to create the model
    validation_data=val_data
)

# Check if weights file exists
if os.path.exists(weights_path):
    model.model.load_weights(weights_path)
    print("Loaded model weights from:", weights_path)

# Define model checkpoint callback to save weights after each epoch
checkpoint_callback = ModelCheckpoint(
    filepath=weights_path,
    save_weights_only=True,
    save_freq='epoch'
)

# Continue training the model
history = model.model.fit(
    train_data, 
    validation_data=val_data, 
    epochs=50,  # Total number of epochs
    callbacks=[checkpoint_callback]
)

# Evaluate the model
model.evaluate(val_data)

# Export the model
model.export(export_dir='.', tflite_filename='/content/gdrive/MyDrive/train_detect_object/best.tflite')
