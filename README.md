# Fault Detection in Air Pressure System

![Truck gif](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdTdoMHV5OG4yOHp5NXYwdnFkY2thYmE1Mmo2dm5ibzJoOGMwZzd0OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/uPQoNeBTTJXXPvRveK/giphy.gif)

### Problem Statement
The Air Pressure System (APS) is a critical component of a heavy-duty vehicle that 
uses compressed air to force a piston to provide pressure to the brake pads, slowing 
the vehicle down. The benefits of using an APS instead of a hydraulic system are the 
easy availability and long-term sustainability of natural air.  
This is a Binary Classification problem, in which the affirmative class indicates that the 
failure was caused by a certain component of the APS, while the negative class 
indicates that the failure was caused by something else.

The problem is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.

## Tech Stack Used
1. Python 
2. FastAPI 
3. Machine learning algorithms
4. Docker
5. MongoDB

## Infrastructure Required.

1. AWS S3
2. AWS EC2
3. AWS ECR
4. Git Actions

## How to run?
Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for data storage. You also need AWS account to access the service like S3, ECR and EC2 instances.

## Project Archietecture
![0_Sensor Training Pipeline (1)](https://github.com/pavankumarchowdary35/Fault-detection-in-Air-Pressure-System/assets/67354434/04b1cb6a-3aed-410f-93d9-bdc5040317a3)



## Deployment Archietecture
![image](https://user-images.githubusercontent.com/57321948/193536973-4530fe7d-5509-4609-bfd2-cd702fc82423.png)


### Step 1: Clone the repository
```bash
git clone https://github.com/pavankumarchowdary35/Fault-detection-in-Air-Pressure-System.git
```

### Step 2- Create a conda environment after opening the repository

```bash
conda create -n sensor python=3.7.6 -y
```

```bash
conda activate sensor
```

### Step 3 - Install the requirements
```bash
pip install -r requirements.txt
```

### Step 4 - Export the environment variable
```bash
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

export AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>

export MONGODB_URL="mongodb+srv://pavankumarmedarametla0605:pavankumar6@cluster0.ldqemc0.mongodb.net/"

```

### Step 5 - Run the application server
```bash
python main.py
```

### Step 6. Train application
```bash
http://localhost:8080/train

```

### Step 7. Prediction application
```bash
http://localhost:8080/predict

```

