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

# Create a new model and load the weights
new_model = object_detector.create(
    train_data, 
    model_spec=spec, 
    batch_size=4, 
    train_whole_model=True, 
    epochs=0,  # Set epochs to 0 because we will load weights
    validation_data=val_data
)

# Load weights from a specific epoch
new_model.load_weights('/content/gdrive/MyDrive/train_detect_object/model_weights_50.h5')  # Adjust the filename as needed

# Define model checkpoint callback to save weights after each epoch
checkpoint_callback = ModelCheckpoint(
    filepath='/content/gdrive/MyDrive/train_detect_object/model_weights_further_{epoch:02d}.h5',
    save_weights_only=True,
    save_freq='epoch'
)

# Continue training the model
new_model = object_detector.create(
    train_data, 
    model_spec=spec, 
    batch_size=4, 
    train_whole_model=True, 
    epochs=20,  # Number of additional epochs you want to train
    validation_data=val_data,
    callbacks=[checkpoint_callback]
)

# Evaluate the model
new_model.evaluate(val_data)

# Export the model
new_model.export(export_dir='.', tflite_filename='/content/gdrive/MyDrive/train_detect_object/best_further_trained.tflite')
