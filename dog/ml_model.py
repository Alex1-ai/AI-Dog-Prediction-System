# ml_model.py
import os

# ⚠️ MUST be set before TensorFlow import
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_NUM_INTRAOP_THREADS"] = "1"
os.environ["TF_NUM_INTEROP_THREADS"] = "1"

from django.conf import settings
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import pandas as pd

# -----------------------------
# Load labels
# -----------------------------
labels_csv = pd.read_csv(settings.LABEL_PATH)
labels = labels_csv["breed"].to_numpy()
unique_breeds = np.unique(labels)

def get_pred_label(prediction_probabilities):
    return unique_breeds[np.argmax(prediction_probabilities)]

# -----------------------------
# Model loader (USED ONCE)
# -----------------------------
def load_model(model_path):
    print(f"Loading saved model from {model_path}")
    return tf.keras.models.load_model(
        model_path,
        custom_objects={"KerasLayer": hub.KerasLayer}
    )

# -----------------------------
# IMAGE PIPELINE
# -----------------------------
IMG_SIZE = 224
BATCH_SIZE = 32

def process_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, [IMG_SIZE, IMG_SIZE])
    return image

def create_data_batches(X, test_data=False):
    data = tf.data.Dataset.from_tensor_slices(tf.constant(X))
    data = data.map(process_image)
    return data.batch(BATCH_SIZE)

# -----------------------------
# 🔥 LOAD MODEL ONCE AT STARTUP
# -----------------------------
print("Initializing ML model...")
MODEL = load_model(settings.MODEL_PATH)

# Warm-up (prevents first-request timeout)
_dummy = np.zeros((1, 224, 224, 3), dtype=np.float32)
MODEL.predict(_dummy)

print("ML model loaded and ready")
