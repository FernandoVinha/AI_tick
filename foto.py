import torch
import cv2
import os

# Load the trained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='runs/train/exp2/weights/best.pt')

# Function to detect ticks, draw rectangles, and display the count
def detect_and_save_all(input_folder, output_folder):
    # Check if the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process all images in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Check if it's an image
            image_path = os.path.join(input_folder, filename)
            save_path = os.path.join(output_folder, filename)

            # Read the image
            img = cv2.imread(image_path)

            # Perform detection
            results = model(image_path)

            # Process the results
            detections = results.xyxy[0].cpu().numpy()  # Format (x1, y1, x2, y2, conf, class)

            # Tick counter
            tick_count = 0

            # Draw rectangles around detected ticks
            for det in detections:
                x1, y1, x2, y2, conf, cls = det
                if conf > 0.25:  # Set a confidence threshold to display the detection
                    tick_count += 1  # Increment tick count
                    # Draw a rectangle around the detected tick
                    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            # Add the total number of detected ticks to the image
            cv2.putText(img, f'Ticks detected: {tick_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Save the image with detections and the total count
            cv2.imwrite(save_path, img)
            print(f"Processed and saved image at: {save_path}")

# Paths for the input image folder and output folder
input_folder = '/object/val'  # Update to the correct path
output_folder = '/object/val_processed'  # Folder where the processed images will be saved

# Run the function to process all images
detect_and_save_all(input_folder, output_folder)