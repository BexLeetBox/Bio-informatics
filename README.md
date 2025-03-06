# Transcription Factor Binding Site Scanner

This project is an interactive tool for **predicting and visualizing transcription factor (TF) binding sites** using **JASPAR motifs**. It integrates **Flask** for the backend, **Plotly** for interactive visualizations, and retrieves TF motifs from **JASPAR’s API**.


# 🚀 Setup Instructions

Follow these steps to set up and run the project using a compatible Python version, recommended version is **Python 3.11** but other versions could work seamlessly. **Step** **1** and **2** can be skipped and are only provided for the sake of convenience. 

## 📌Prerequisites

- **Python 3.11** installed on your system. Compatibility of the project other than this version was not tested, but lower versions should also work for the most part. 
- To check if Python 3.11 is installed, run: 
```sh
python --version
```

## 🔧Step 1: Create a virtual environment

All your files and folders are presented as a tree in the file explorer. You can switch from one to another by clicking a file in the tree.
1. Open a terminal (Command Prompt or PowerShell).
2. Navigate to the project directory by running the following command where you replace path/to/your/project with your project directory path:
 ```sh
cd path/to/your/project
```
3. Create a virtual environment using **Python 3.11**:
 ```sh
python -m venv venv
```





## ▶️Step 2: Activate the Virtual Environment

On the same Command Prompt window from **step 1** type in:
 ```sh
venv\Scripts\activate
```
Note: "Scripts" might be "bin" depending on your Python version, but for version **3.11** it should be Scripts  

## 📦Step 3: Install Dependencies
Run the following command to install all required packages:
 ```sh
pip install -r requirements.txt
```

## 🏃Step 4: Run the project
Start the Flask server by running from the project root directory:
 ```sh
python app.py
```

# 📝Troubleshooting

## **Encountering `distutils` Not Found error?**

If you encounter, ````ModuleNotFoundError: No module named 'distutils'````, it is very likely that you are not using python 3.11. You can check which python version you have by running:
 ```sh
python --version
```
If this does not display 3.11 or a compatible Python version, like 3.12 which does not have setuptools wheel installed, even after installing Python 3.11, you can use the following command to locate the correct version:
 ```sh
where.exe python
```
This should show Python 311 in one of the paths shown with the command. Copy this path and create the virtual environment from step 1 this way:
 ```sh
C:\copied\path\to\python.exe -m venv venv
```
After that, redo the steps and the project should work.
