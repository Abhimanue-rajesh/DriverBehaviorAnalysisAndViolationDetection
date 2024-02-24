# DriverBehaviorAnalysisAndViolationDetection
Driver Behavior Analysis And Violation Detection


## Project Initialization 

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

## Data Set

1. To clean the data 
- *Before cleaning the database change the directory name in the script*
```bash
  python data_pre_processing.py
```

2. To get more data through web scrapping with microsoft edge
```bash
  python web_scraping_image.py
```