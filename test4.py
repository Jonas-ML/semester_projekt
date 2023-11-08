import os
import time
import datetime
from jetson_inference import detectNet
from jetson_utils import videoSource, saveImage, cudaAllocMapped, cudaCrop, cudaDeviceSynchronize

# Configuration parameters (hard-coded for simplicity)
model = "ssd-mobilenet-v2"  # Pre-trained model
threshold = 0.5  # Minimum detection threshold
camera = "/dev/video0"  # Camera device
output_dir = "images/test/detections"  # Directory to save snapshots
overlay = "box,labels,conf"  # Detection overlay flags

# Create output directory for snapshots
os.makedirs(output_dir, exist_ok=True)

# Initialize video source
input_stream = videoSource(camera)

# Load the object detection network
net = detectNet(model, threshold=threshold)

# Process frames until the stream ends
while True:
    # Capture the next image frame
    img = input_stream.Capture()

    # Detect objects in the image
    detections = net.Detect(img, overlay=overlay)

    # Print the number of objects detected
    print("Detected {} objects in image".format(len(detections)))

    # Save snapshots for each detected object
    for idx, detection in enumerate(detections):
        # Create the ROI for the detected object
        roi = (int(detection.Left), int(detection.Top), int(detection.Right), int(detection.Bottom))
        # Allocate CUDA memory for the snapshot
        snapshot = cudaAllocMapped(width=roi[2]-roi[0], height=roi[3]-roi[1], format=img.format)
        # Crop and save the image of the detected object
        cudaCrop(img, snapshot, roi)
        cudaDeviceSynchronize()
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        saveImage(os.path.join(output_dir, "{}-{}.jpg".format(timestamp, idx)), snapshot)
        # Free CUDA memory
        del snapshot

    # Exit on end of input stream
    if not input_stream.IsStreaming():
        break

    # Wait for 5 seconds
    time.sleep(5)

