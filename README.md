<h1 align="center">Drowsiness Detection Model</h1>

The project utilizes machine learning models deployed on a _Raspberry Pi_ to monitor driver behavior and detect violations such as **drowsiness, mobile phone usage, speeding, alcohol consumption, and seat belt negligence**. The system integrates camera input, sensor data processing, and email notification capabilities for proactive enforcement of traffic regulations and prevention of accidents.

## Key Components 
1. Machine Learning Models
  - Utilizes YOLOv5 models for drowsiness detection and cell phone usage detection.
  - Pretrained models are loaded to identify relevant objects in real-time camera streams.

2. Image Processing
  - Captures images using the Raspberry Pi camera module.
  - Processes images to identify violations such as drowsiness and mobile phone usage.
  - Saves violation evidence images for further analysis and reporting.

3. Sensor Data Processing
  - Monitors sensor data including speed, alcohol levels, and seat belt usage.
  - Processes sensor inputs to detect violations such as over speeding and alcohol consumption.
  - Implements logic to detect overtaking on the wrong side using IR sensors.

4. Email Notification System
  - Sends email notifications with violation details and evidence attachments.
  - Alerts authorities or designated individuals in real-time for timely intervention.

## Implementation Details:

  - The system runs on a Raspberry Pi, ensuring portability and ease of deployment in vehicles.
  - Multithreading is utilized to simultaneously handle machine learning predictions and sensor data processing for real-time monitoring.
  - GPIO pins are utilized for interfacing with sensors and controlling external devices like the LCD screen.
  - Violation thresholds are set to trigger email notifications for repeated offenses, enhancing enforcement effectiveness.
  - The predictions from the machine learning models **will not be 100% accurate** and will be dependent on lighting and other conditions

## Connections

  > Connect the wires and cables carefully. Make sure not to damage any component

  ### Alcohol Sensor
    - The digital pin should be connected to the GPIO-18
  
  ### Seatbelt 
    - The seatbelt pin should be connected to the GPIO-26
  
  ### IR Sensor
    - The right side IR sensor should be connected to GPIO-23
    - The left side IR sensor should be connected to GPIO-24

  ### Rotary Encoder
    - The rotary encoder for overspeed detection should be connected to
      Clock - GPIO-7
      Dt-Pin - GPIO-8 

  **Double Check all the connections before turing on the power - ensure all the vcc and ground pins are connected**

## Running main.py
  - Turn on the system and connect all the sensors 
  - Connect to raspberry pi through putty with shh
  - Navigate to the DriverBehaviorAnalysisAndViolationDetection
  ```bash
  cd Desktop
  ```
  ```bash
  cd DriverBehaviorAnalysisAndViolationDetection
  ```
  - Activate the virtual environment
  ```bash
  . venv/bin/activate
  ```
  - Run the main.py file 
  ```bash
  python main.py
  ```

## Conclusion  

The Driver Safety Monitoring System leverages machine learning and sensor technologies to enhance road safety by detecting and addressing driver violations in real-time. By integrating intelligent monitoring capabilities with email notifications, the system enables proactive intervention to prevent accidents and promote responsible driving behavior.