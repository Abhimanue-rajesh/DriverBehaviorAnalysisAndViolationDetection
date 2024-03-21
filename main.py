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
from RPLCD.i2c import CharLCD
import threading

# # Loading the Machine Learning Models
# # Model for Drowsyness detection 
drowsy_detection_model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5_d_and_n/runs/train/exp9/weights/last.pt', force_reload=True)
# # Model for Cell phone detection 
cell_detection_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Creating Output directories for the image storage
image_output_directory = 'image_output_directory'
violation_data_storage = 'violation_data_storage'

os.makedirs(image_output_directory, exist_ok=True)
os.makedirs(violation_data_storage, exist_ok=True)

# Initialize counter variable for violations
drowsy_mobile_violation_counter = 0
alcohol_violation = 0 
over_speed_violation = 0 
seat_belt_violation = 0
over_speed_violation = 0 
alcohol_violation = 0 
seat_belt_violation = 0

# LCD initialization 
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)

# Initialize the camera to capture images for machine learning models
pi_camera = Picamera2()
config = pi_camera.create_preview_configuration()
config["transform"] = libcamera.Transform(hflip=1, vflip=1)
pi_camera.configure(config)
pi_camera.start(show_preview=True)

def SendEmail(message,include_attachment=False):
    # Create multipart message
    msg = MIMEMultipart()
    msg['Subject'] = "Violation Detected by AI Model"
    msg['To'] = "abhimanuemvk@gmail.com"
    msg['From'] = "driverviolation@gmail.com"

    # Attach message body
    msg.attach(MIMEText(message, 'plain'))

    if include_attachment == True:
        # Attach files in the directory
        for filename in os.listdir("violation_data_storage"):
            filepath = os.path.join("violation_data_storage", filename)
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
    gmail.login("driverviolation@gmail.com", "kege mleo pruw znbl")
    # Sending mail
    gmail.send_message(msg)

def CheckViolations():
    if drowsy_mobile_violation_counter >= 3:
        print('3 Violations Detected taking action')
        message = "A violation has been detected and the necessary proof has been attached with this email, This is a machine generated message, DO NOT REPLY"
        SendEmail(message, include_attachment=True)
        

def PredictDrowsiness(image_array):
    global drowsy_mobile_violation_counter

    # Converting the image to RGB.
    rgb_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    # Passing the rgb image to the model to get the prediction.
    drowsiness_detection_model_result = drowsy_detection_model(rgb_image)
    # Get all the detection from the model
    all_model_detections = drowsiness_detection_model_result.pandas().xyxy[0]
    
    # Loop through each detections to check for the name drowsy.
    for index, obj in all_model_detections.iterrows():
        class_name = obj['name']

        if class_name == 'drowsy':
            print('Drowsy person detected')
            # Get current timestamp for unique file naming
            timestamp = int(time.time())
            # Generate unique file name using timestamp
            image_path = os.path.join(violation_data_storage, f"drowsiness_{timestamp}_{index}.jpg")
            # Save the image with the generated file name
            cv2.imwrite(image_path, image_array)
            print(f"Violation image saved: {image_path}")
            drowsy_mobile_violation_counter += 1
            CheckViolations()
        else:
            break
    
def PredictCellPhoneUsage(image, image_array):
    global drowsy_mobile_violation_counter

    # Passing the image to the model to get the prediction
    cell_detection_model_result = cell_detection_model(image)
    # Get all the detection from the model
    all_model_detected_objects = cell_detection_model_result.pandas().xyxy[0]

    # Loop through each detected object
    for index, obj in all_model_detected_objects.iterrows():
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
            drowsy_mobile_violation_counter += 1
            CheckViolations()
        else:
            break

def MachineLearningPredictions():
    try:
        while True:
            image = pi_camera.capture_image('main') # Capturing Image
            image_array = np.array(image) # Converting to NP Array 
            image_path = os.path.join(image_output_directory, "captured_image.jpg") #defining image path
            cv2.imwrite(image_path, image_array) # Writing image to created directory

            # Passing the image and its array to cellphone and prediction drowsiness models
            PredictDrowsiness(image_array)
            PredictCellPhoneUsage(image_path, image_array)

            # Sleeping for 10 seconds to reduce cpu load
            time.sleep(10)

    except KeyboardInterrupt:
        print('Key Board Interrupt - Breaking Program - Camera')
        pi_camera.close()

wrong_side_violation = 0

def OverTake(start_time):
    global wrong_side_violation
    while True:
        ir_sensor_right = GPIO.input(23)
        current_time = time.perf_counter()      
        elapsed_time = current_time - start_time
        
        if ir_sensor_right == 0:
            lcd.clear()
            lcd.cursor_pos = (0,1)
            lcd.write_string('TIMED OVERTAKE')
            time.sleep(3)
            break

        if elapsed_time > 10 and ir_sensor_right == 1:
            print('Time out')
            lcd.clear()
            lcd.cursor_pos = (0,1)
            lcd.write_string('WRONG SIDE FOR')
            lcd.cursor_pos = (1,0)
            lcd.write_string('MORE THAN 10 SEC')
            wrong_side_violation += 1
            if wrong_side_violation >= 3:
                print('sending email')
                SendEmail(message="Driver is detected using the wrong line for more than 10 seconds, Times Violated = 3")
            time.sleep(3)
            break




def SensorDataPossessing():
    global over_speed_violation
    global alcohol_violation
    global seat_belt_violation

    CLK_PIN = 7   
    DT_PIN = 8    
    SW_PIN = 25   

    # Initializing variables
    counter = 0
    CLK_state = 0
    prev_CLK_state = 0

    # Configure GPIO pins
    GPIO.setmode(GPIO.BCM)

    # GPIO setup for rotary encoder
    GPIO.setup(CLK_PIN, GPIO.IN)
    GPIO.setup(DT_PIN, GPIO.IN)
    GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # GPIO for Alcohol sensor
    GPIO.setup(18, GPIO.IN)

    # GPIO For seatbelt
    GPIO.setup(26, GPIO.IN) 

    GPIO.setup(23, GPIO.IN) 
    GPIO.setup(24, GPIO.IN) 

    # Read the initial state of the rotary encoder's CLK pin
    prev_CLK_state = GPIO.input(CLK_PIN)

    right_ir_first_crossing = False

    try:
        while True:
            # Initializing input
            CLK_state = GPIO.input(CLK_PIN) # Rotary Encoder
            alcohol_level = GPIO.input(18) # Alcohol Sensor
            
            seat_belt = GPIO.input(26) # IR for seatbelt
            
            ir_sensor_right = GPIO.input(23) # IR Sensor
            ir_sensor_left = GPIO.input(24) # IR Sensor
                 
            
            if seat_belt == 0:
                if CLK_state != prev_CLK_state and CLK_state == GPIO.HIGH:
                    
                    if GPIO.input(DT_PIN) == GPIO.HIGH:
                        counter -= 10
                    else:
                        counter += 10
                    
                    to_display = f'Speed: {counter}'
                    lcd.clear()
                    lcd.cursor_pos = (0,0)
                    lcd.write_string(to_display)
                    if counter > 60:
                        lcd.cursor_pos = (1,0)
                        lcd.write_string('Over Speed')
                        over_speed_violation += 1
                        if over_speed_violation >=3:
                            print('sending email')
                            SendEmail(message="Driver is Over Speeding, Times Violated = 3")
                    else:
                        lcd.cursor_pos = (1,0)
                        lcd.write_string('Normal Speed')
                
                # Save last CLK state
                prev_CLK_state = CLK_state

                #alcohol sensor
                if alcohol_level == 0:
                    lcd.clear()
                    lcd.cursor_pos = (0,0)
                    lcd.write_string('Alcohol Present!')
                    alcohol_level += 1
                    if alcohol_level >= 1:
                        print('sending email')
                        SendEmail(message="Driver is detected using alcohol")
                    time.sleep(0.5)
                
                    

                if ir_sensor_right == 0 :
                    print('First Ir crossed')
                    right_ir_first_crossing = True

                if ir_sensor_left == 0 and right_ir_first_crossing == True:
                    print('Second Ir crossed')
                    lcd.clear()
                    lcd.cursor_pos = (0,3)
                    lcd.write_string('OVERTAKING!')
                    start_time = time.perf_counter()
                    OverTake(start_time)  
                    
            else:
                print('No seat belt')
                lcd.cursor_pos = (0,2)
                lcd.write_string('NOT WEARING')
                lcd.cursor_pos = (1,3)
                lcd.write_string('SEAT BELT')
                seat_belt_violation += 1

                if seat_belt_violation == 3:
                    print("sending email")
                    SendEmail(message="Driver Detected not using a seatbelt , Times Violated = 3")
                time.sleep(0.5)
            
                    
    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up GPIO on program exit
        lcd.close(clear=True)


if __name__ == "__main__":
    machine_learning_thread = threading.Thread(target=MachineLearningPredictions)
    sensor_thread = threading.Thread(target= SensorDataPossessing)

    machine_learning_thread.start()
    sensor_thread.start()
    print('Program Started')