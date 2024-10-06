#!/bin/bash

# Define directory variables
PROJECT_DIR="$(pwd)"  # The current directory of the project
VENV_DIR="venv"  # Virtual environment directory
YOLOV5_DIR="$PROJECT_DIR/yolov5"  # YOLOv5 directory
DATA_YAML="$PROJECT_DIR/tick_dataset.yaml"  # Path to dataset configuration file
PRETRAINED_WEIGHTS="yolov5s.pt"  # Pretrained weights to use

# Training parameters
IMAGE_SIZE=1024
BATCH_SIZE=16
EPOCHS=200

# Function to check for errors
check_error() {
    if [ $? -ne 0 ]; then
        echo "Error during the process. Exiting."
        exit 1
    fi
}

# Activate the virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "Activating the virtual environment..."
    source $VENV_DIR/bin/activate
    check_error
else
    echo "Virtual environment not found. Please run setup_project.sh first."
    exit 1
fi

# Check if YOLOv5 directory exists
if [ ! -d "$YOLOV5_DIR" ]; then
    echo "YOLOv5 directory not found. Please ensure YOLOv5 is set up correctly."
    exit 1
fi

# Check if the dataset YAML exists
if [ ! -f "$DATA_YAML" ]; then
    echo "Dataset YAML file not found at $DATA_YAML."
    exit 1
fi

# Start training
echo "Starting YOLOv5 training with the following parameters:"
echo "Image size: $IMAGE_SIZE"
echo "Batch size: $BATCH_SIZE"
echo "Epochs: $EPOCHS"
echo "Using pretrained weights: $PRETRAINED_WEIGHTS"
echo "Dataset configuration file: $DATA_YAML"

cd $YOLOV5_DIR

python train.py --img $IMAGE_SIZE --batch $BATCH_SIZE --epochs $EPOCHS --data $DATA_YAML --weights $PRETRAINED_WEIGHTS

# Check if training completed successfully
if [ $? -eq 0 ]; then
    echo "Training completed successfully!"
else
    echo "Training failed."
    exit 1
fi

# Deactivate the virtual environment
deactivate

echo "Training script finished."
