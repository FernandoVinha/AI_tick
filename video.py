import torch
import cv2
import os
from sort import Sort  # SORT tracking library

# Load the trained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='runs/train/exp2/weights/best.pt')

# Function to detect ticks in video and save the video with detections and tracking
def detect_and_track_video(input_video_path, output_video_path):
    # Initialize the SORT tracker
    tracker = Sort()

    # Read the video
    cap = cv2.VideoCapture(input_video_path)

    # Get original video information (width, height, frames per second)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create the output video file
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Process each frame of the video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Exit loop if no more frames

        # Perform detection on the frame
        results = model(frame)
        detections = results.xyxy[0].cpu().numpy()  # Format (x1, y1, x2, y2, conf, class)

        # Prepare detections for the tracker (format [x1, y1, x2, y2, score])
        dets = []
        for det in detections:
            x1, y1, x2, y2, conf, cls = det
            if conf > 0.25:  # Only consider detections with confidence greater than 0.25
                dets.append([x1, y1, x2, y2, conf])

        dets = np.array(dets)

        # Update the tracker with the new detections
        tracks = tracker.update(dets)

        # Draw bounding boxes around the ticks and track the IDs
        for track in tracks:
            x1, y1, x2, y2, track_id = track.astype(int)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'ID: {track_id}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Add logic to check for movement, for example, using past positions

        # Write the processed frame to the output video file
        out.write(frame)

    # Release resources
    cap.release()
    out.release()
    print(f"Processed video saved at: {output_video_path}")

# Paths for input and output video
input_video_path = 'path/to/your/video.mp4'
output_video_path = 'path/to/save/processed_video_with_tracking.mp4'

# Run the function to process the video
detect_and_track_video(input_video_path, output_video_path)
