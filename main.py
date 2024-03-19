from picamera2 import Picamera2
import libcamera
import torch
import os
import cv2
import time
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import RPi.GPIO as GPIO

# Output directories for the image storage
image_output_directory = 'image_output_directory'
violation_data_storage = 'violation_data_storage'

# Initialize counter variable for violations
total_violations = 0

def send_email(email,directory):
    from_email = "driverviolation@gmail.com"
    from_password = "kege mleo pruw znbl"
    to_email = email


    subject = "Violation Deteced by AI Model"
    message = "A violation has been detected and the nessesary proof has been attached with this email, This is a machine generated message, DO NOT REPLY"

    # Create multipart message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    # Attach message body
    msg.attach(MIMEText(message, 'plain'))

    # Attach images
    # Attach files in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as f:
                attachment = MIMEImage(f.read())
                attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(attachment)

    # Create SMTP session for sending the mail
    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    # Login to gmail account
    gmail.login(from_email, from_password)
    # Send mail
    gmail.send_message(msg)

def check_number_of_violations():
    if total_violations >= 1:
        print('Violations limit reach')
        email = "abhimanuemvk@gmail.com"
        directory = "violation_data_storage"
        send_email(email,directory)

def check_drowsiness(image_array):
    global total_violations 
    # Loading the yolov5 cell_detection_model for cell phone detection
    drowsy_detection_model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5_d_and_n/runs/train/exp9/weights/last.pt', force_reload=True)
    print('Predicting drowsiness with the image.')
    converted_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB) 
    results = drowsy_detection_model(converted_image)
    detections = results.pandas().xyxy[0]

    ## Loop through each detections
    for index, obj in detections.iterrows():
        class_name = obj['name']

        if class_name == 'drowsy':
            print('Drowsy person detected')
            # Get current timestamp for unique file naming
            timestamp = int(time.time())
            # Generate unique file name using timestamp
            image_path = os.path.join(violation_data_storage, f"drowsines_{timestamp}_{index}.jpg")
            # Save the image with the generated file name
            cv2.imwrite(image_path, image_array)
            print(f"Violation image saved: {image_path}")
            total_violations += 1
            check_number_of_violations()
        else:
            break

def check_cell_phone(image, image_array):
    global total_violations 

    # Loading the yolov5 cell_detection_model for cell phone detection
    cell_detection_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    results = cell_detection_model(image)
    print('Predicting cell phone usage with the image.')
    detected_objects = results.pandas().xyxy[0]
    
    # To store the captured violations
    os.makedirs(violation_data_storage, exist_ok=True)
    
    ## Loop through each detected object
    for index, obj in detected_objects.iterrows():
        class_name = obj['name']

        if class_name == 'cell phone':
            print('Cell phone detected')
            # Get current timestamp for unique file naming
            timestamp = int(time.time())
            # Generate unique file name using timestamp
            image_path = os.path.join(violation_data_storage, f"cell_phone_usage{timestamp}_{index}.jpg")
            # Save the image with the generated file name
            cv2.imwrite(image_path, image_array)
            print(f"Violation image saved: {image_path}")
            total_violations += 1
            check_number_of_violations()
        else:
            break


def start_camera():
    pi_camera = Picamera2()
    config = pi_camera.create_preview_configuration()
    config["transform"] = libcamera.Transform(hflip=1, vflip=1)
    pi_camera.configure(config)
    pi_camera.start(show_preview=True)

    try:
        while True:
            print('Capturing Image')
            image = pi_camera.capture_image('main')
            image_array = np.array(image)

            # To store the captured images
            os.makedirs(image_output_directory, exist_ok=True)

            image_path = os.path.join(image_output_directory, "captured_image.jpg")
            cv2.imwrite(image_path, image_array)
            print('Temporary image stored to directory')
            check_cell_phone(image_path, image_array)
            check_drowsiness(image_array)
            time.sleep(8)

    except KeyboardInterrupt:
        pi_camera.close()

start_camera()


def speed_sensor():
    print('starting speed sensor!')
    # Pin numbers on Raspberry Pi
    CLK_PIN = 7   # GPIO7 connected to the rotary encoder's CLK pin
    DT_PIN = 8    # GPIO8 connected to the rotary encoder's DT pin
    SW_PIN = 25   # GPIO25 connected to the rotary encoder's SW pin

    counter = 0
    CLK_state = 0
    prev_CLK_state = 0

    prev_button_state = GPIO.HIGH

    # Configure GPIO pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CLK_PIN, GPIO.IN)
    GPIO.setup(DT_PIN, GPIO.IN)
    GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Read the initial state of the rotary encoder's CLK pin
    prev_CLK_state = GPIO.input(CLK_PIN)

    try:
        while True:
            # Read the current state of the rotary encoder's CLK pin
            CLK_state = GPIO.input(CLK_PIN)

            # If the state of CLK is changed, then pulse occurred
            # React to only the rising edge (from LOW to HIGH) to avoid double count
            if CLK_state != prev_CLK_state and CLK_state == GPIO.HIGH:
                # If the DT state is HIGH, the encoder is rotating in counter-clockwise direction
                # Decrease the counter
                if GPIO.input(DT_PIN) == GPIO.HIGH:
                    counter -= 10
                else:
                    # The encoder is rotating in clockwise direction => increase the counter
                    counter += 10

                if counter >= 60:
                    print('Over Speed Detected , Slow Down')
                else:
                    print('Normal Driving')

                print("count:" , counter)

            # Save last CLK state
            prev_CLK_state = CLK_state

            # State change detection for the button
            button_state = GPIO.input(SW_PIN)
            if button_state != prev_button_state:
                time.sleep(0.01)  # Add a small delay to debounce

            prev_button_state = button_state

    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up GPIO on program exit


# speed_sensor()

def alcohol_sensor():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN)

    while True:
        alcohol_level = GPIO.input(18)
        print(alcohol_level)
        if alcohol_level == 0:
            print('Alcohol Presence Detected')
        elif alcohol_level == 1 :
            print('No Alcohol Presence')

# alcohol_sensor()

def whiteline_crossing():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN) 
    GPIO.setup(24, GPIO.IN)  

    # Initializeing variables
    right_line_first_crossing_detected = False
    left_line_first_crossing_detected = False
    left_line_second_crossing_detected = False
    vehicle_crossed = False

    try:
        while True:
            ir_sensor_right = GPIO.input(23)
            ir_sensor_left = GPIO.input(24)

            if ir_sensor_right == 0 and vehicle_crossed == False:
                right_line_first_crossing_detected = True
                print("Right sensor First")

            if ir_sensor_left == 0 and vehicle_crossed == False:
                left_line_first_crossing_detected = True
                print("Left sensor First")

            if right_line_first_crossing_detected and left_line_first_crossing_detected:
                print('Vehicle Crossed the white line')
                time_when_crossed = time.perf_counter()
                vehicle_crossed = True
                right_line_first_crossing_detected = False
                left_line_first_crossing_detected = False

            if vehicle_crossed and ir_sensor_left == 0:
                left_line_second_crossing_detected = True
                vehicle_crossed = False
                print("Left sensor second ")

            if left_line_second_crossing_detected and ir_sensor_right == 0:
                print("Vehicle back on track")
                time_back_on_track = time.perf_counter()
                total_time = time_back_on_track - time_when_crossed
                print(total_time)
                break


            # Sleep for a short duration to avoid CPU hogging
            time.sleep(0.1)

    except KeyboardInterrupt:
        GPIO.cleanup()

        
# whiteline_crossing()