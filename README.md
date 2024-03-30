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

## 1. Collect Data (Windows)

- To collect the image data to train the new model you can run the RealTimeDataCollection.ipynb 
- Follow the instructions in the jupiter notebook

> This will collect and name the images and store the images in the directory

## 2. To Retrain the model

### 2.1. Setting up the project and labeling the data

#### 2.1.1. Creating a virtuelenv and installing all the required libraries

```bash
pip install install torch torchvision torchaudio -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html
```

- Clone the ultralytics yolo v5 model from github

```bash
git clone https://github.com/ultralytics/yolov5
```

- Then change the directory to the yolov5 directory and install the required packages 

```bash
cd yolov5
```

```bash
pip install -r requirements.txt
```

#### 2.1.2. Installing the labeling GUI
- Clone the labelimg from github
```bash
git clone https://github.com/tzutalin/labelImg
```

- Install a package and upgrade them 
```bash
pip install pyqt5 lxml --upgrade
```

- Change the directory to labelImg
```bash
cd labelImg
```

- Install other dependencies for labelImg

```bash
pyrcc5 -o libs/resources.py resources.qrc
```
- To label images run 
```bash
python labelImg.py
```
- Choose the file with the images 
- Choose the file to output the labels
- Move right and left with D and A Keys 
- Mark the areas with the W key 

### 2.2. After setting up the project, installing the libraries and labeling the images

- To train the model on the new data set prepare a new dataset.yml file 
- Change the directory to yolov5 

```bash
cd yolov5
```

- Train the model with this command

```bash
python train.py --img 320 --batch 16 --epochs 105 --data dataset.yml --weights yolov5s.pt --workers 2
```

- This command will initiate training using the train.py file within the yolov5 framework.
- "--img 320" specifies the size of the images (not the number of images) used for training.
- "--batch 16" sets the batch size for training data.
- "--epochs 500" determines the number of iterations over the dataset during training.
- "--data dataset.yml" indicates the YAML file containing dataset information, including class labels.
- "--weights yolov5s.pt" specifies the pre-trained YOLOv5 model to be used for transfer learning.
- "--workers 2" limits the number of PyTorch workers used during training.

## 3. Test the trained model

> To test your trained model with the device camera (Windows)

- To test the model open the TestCustomModel.ipynb in an IDE
- Run the code line by line 

## 4. Additional Scripts For Data Collection and Manipulation


### 4.1. Scrapping data from the web with bing

- This script will ask to enter the image category that you want to download 

```bash
python script/data_scraping.py
```

### 4.2. Preprocessing the data before training

- Change the path to the directory you want to do the preprocessing

```bash
python script/data_preprocessing.py
```

### 4.3. Remove duplicate images from the dataset

- Change the path to the directory you want to check for duplicates

```bash
python script/data_duplicate.py
```

### 4.4. Manipulate the image contrast 

- Change the path to the data directory
- This will create two directories with the contrast increased and decreased images

```bash
python script/image_contrast.py
```

### 4.5. Manipulate the image by flipping the image 

- Change the path to the data directory

```bash
python script/image_flip.py
```

### 4.6. Manipulate the image by rotation 

- Change the path to the data directory
- Change the degree of rotation as needed
- Will also create a output directory for all the rotated images

```bash
python script/image_rotation.py
```

## Conclusion  

The Driver Safety Monitoring System leverages machine learning and sensor technologies to enhance road safety by detecting and addressing driver violations in real-time. By integrating intelligent monitoring capabilities with email notifications, the system enables proactive intervention to prevent accidents and promote responsible driving behavior.