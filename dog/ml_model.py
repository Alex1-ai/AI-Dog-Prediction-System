from django.conf import settings
# Import Tensorflow into colab
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import pandas as pd

tf.config.set_visible_devices([], 'GPU')

labels_csv = pd.read_csv(settings.LABEL_PATH)


labels = labels_csv["breed"].to_numpy()
unique_breeds = np.unique(labels)


def get_pred_label(prediction_probabilities):
  """

  Turn an array of prediction probabilities into a label.

  """
  return unique_breeds[np.argmax(prediction_probabilities)]

# create a function to load a model
def load_model(model_path):
    """
    Loads a saved model from a specified path.
    """
    print(f"Loading saved model from {model_path}")
    model = tf.keras.models.load_model(model_path,
                                       custom_objects={"KerasLayer": hub.KerasLayer})
    return model




## TUrning our data into batches
def get_image_label(image_path, label):
  """
   Take an image file path name and the associated label, processes the image and return a type of image,lable

  """

  image = process_image(image_path)
  return image, label

# Define image size
IMG_SIZE = 224

# Create a function for preprocessing images
def process_image(image_path, img_size =IMG_SIZE):
  """
    Takes an image file path and turns the image into a Tensor.
  """
  # read in an image file
  image = tf.io.read_file(image_path)
  # turn the jpeg image into numerical Tensor with 3 olour channels(red, green , blue)
  image = tf.image.decode_jpeg(image, channels=3)
  # Convert the colour channel values from 0-255 to 0-1
  image = tf.image.convert_image_dtype(image, tf.float32)
  # Resize the image to our desired value (224,224)
  image = tf.image.resize(image, size=[IMG_SIZE, IMG_SIZE])

  return image


# Define the batch size, 32 is a good start
BATCH_SIZE = 32

# Create a function to turn data into batches
def create_data_batches(X, y=None, batch_size=BATCH_SIZE, valid_data=False, test_data=False):
  """

  Creates batches of data out of image (X) and label (y) pairs.
  Shuffles the data if it's training data but doesn't shuffle if it'ss validation data
  Also accepts test data as input (no labels)
  """
  # If the data is a test dataset, we probably don't have labels
  if test_data:
    print("Creating test data batches...")
    data  = tf.data.Dataset.from_tensor_slices((tf.constant(X))) # only filepaths (no labels)
    data_batch = data.map(process_image).batch(BATCH_SIZE)
    return data_batch

  # IF the data is a valid dataset, we don't need to shuffle it
  elif valid_data:
    print("Creating validation data batches...")
    data = tf.data.Dataset.from_tensor_slices((
                                            tf.constant(X),# filepath
                                            tf.constant(y) # labels
                                               ))
    data_batch = data.map(get_image_label).batch(BATCH_SIZE)
    return data_batch
  else:
    print("Creating training data batches...")
    # TUrn filepaths and labels into Tensors
    data = tf.data.Dataset.from_tensor_slices((tf.constant(X),
                                               tf.constant(y)))
    # Shuffling pathnames and labels before mapping image processor function is faster than shuffling images
    data = data.shuffle(buffer_size=len(X))
    # Create (image, label) tuples (this also turns the image path into a preprocessed image )
    data = data.map(get_image_label)

    # Turn the training data into batches
    data_batch = data.batch(BATCH_SIZE)
  return data_batch




# def make_prediction():
#   # Turn custom images into batch datasets
#   custom_data = create_data_batches(custom_image_paths, test_data=True)
#   custom_data

#   # Make predictions on the custom data
#   custom_preds = loaded_full_model.predict(custom_data)
#   # Get custom image prediction lbels
#   custom_preds_labels = [get_pred_label(custom_preds[i]) for i in range(len(custom_preds))]
#   print(custom_preds_labels)


