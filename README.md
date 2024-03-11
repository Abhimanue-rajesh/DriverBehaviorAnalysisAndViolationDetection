# DriverBehaviorAnalysisAndViolationDetection
Driver Behavior Analysis And Violation Detection


## 1. Project Initialization 

To initialize and set up the code base

1. Ensure Python is downloaded 

```bash
  python --version
```
*Ensure You Have python version 3.11 or above.*

2. Install Virtual Environment

```bash
  pip install virtualenv
```

3. Create a Virtual Environment

```bash
  virtualenv venv
```

4. Activate the Virtual Environment 

```bash
  venv\scripts\activate
```

5. Installing the Required Libraries and Modules

```bash
  pip install -r requirements.txt
```

## 2. Data Set

1. To get more data through web scrapping with microsoft edge
```bash
  python web_scraping_image.py
```

2. To clean the data 
- *Before cleaning the database change the directory name in the script*
```bash
  python data_pre_processing.py
```

3. We will be using parts of this dataset so the paper has to be mentioned in the documentation 

```bash
https://github.com/bindujiit/Driver-Drowsiness-Dataset-D3S-
```
- Gupta, I., Garg, N., Aggarwal, A., Nepalia, N., & Verma, B. (2018, August). Real-time driver's drowsiness monitoring based on dynamically varying threshold. In 2018 Eleventh International Conference on Contemporary Computing (IC3) (pp. 1-6). IEEE

## 3. To test sent email 

- Sign in to gmail account (driverviolation@gmail.com)
- Open Settings 
- Ensure that the two step verification is enabled 
- Search for app password
- Create an app password 
- Copy and paste the key to the script
 
```bash
python sent_email.py  
```
## 3. Face_Detection Model 

- To Detect the faces and to process the data accordingly we will be using a pre trained model.
