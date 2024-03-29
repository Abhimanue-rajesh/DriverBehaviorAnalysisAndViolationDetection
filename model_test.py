import tensorflow as tf
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import time

ml_model = load_model(os.path.join('models','driver_violation_v6.h5'))

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)


def predict(resized_frame):
    # Your detection code here (assuming ml_model and resized_frame are defined)
    ml_model_result = ml_model.predict(np.expand_dims(resized_frame/255, 0))
    
    print(ml_model_result)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the frame to RGB format
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    resized_frame = tf.image.resize(frame, (256,256))

    predict(resized_frame)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()