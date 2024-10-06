#!/bin/bash

# Define directory variables
PROJECT_DIR="$(pwd)"  # Current directory, you can modify as needed
YOLOV5_REPO="https://github.com/ultralytics/yolov5"
LABELIMG_REPO="https://github.com/tzutalin/labelImg"
VENV_DIR="venv"

# Function to check for errors
check_error() {
    if [ $? -ne 0 ]; then
        echo "Error during the process. Exiting."
        exit 1
    fi
}

# Update and install system dependencies for LabelImg
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y pyqt5-dev-tools python3-lxml
check_error

# Clone YOLOv5 repository if not already cloned
if [ ! -d "$PROJECT_DIR/yolov5" ]; then
    echo "Cloning YOLOv5 repository..."
    git clone $YOLOV5_REPO
    check_error
else
    echo "YOLOv5 already cloned."
fi

# Clone LabelImg repository if not already cloned
if [ ! -d "$PROJECT_DIR/labelImg" ]; then
    echo "Cloning LabelImg repository..."
    git clone $LABELIMG_REPO
    check_error
else
    echo "LabelImg already cloned."
fi

# Create and activate virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
    check_error
else
    echo "Virtual environment already exists."
fi

echo "Activating virtual environment..."
source $VENV_DIR/bin/activate
check_error

# Install YOLOv5 dependencies
echo "Installing YOLOv5 dependencies..."
pip install -r yolov5/requirements.txt
check_error

# Install LabelImg dependencies
echo "Installing LabelImg dependencies..."
pip install -r labelImg/requirements/requirements-linux-python3.txt
check_error

# Install project dependencies from requirements.txt
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo "Installing project dependencies..."
    pip install -r $PROJECT_DIR/requirements.txt
    check_error
else
    echo "requirements.txt not found in the project directory."
    exit 1
fi

# Compile and run LabelImg (optional)
echo "Compiling and running LabelImg..."
cd labelImg
make qt5py3
check_error

echo "LabelImg installed and ready to use. To run manually, execute: python3 labelImg.py"

# Go back to project directory
cd "$PROJECT_DIR"

echo "Setup complete. YOLOv5 and LabelImg have been successfully set up in the virtual environment."
