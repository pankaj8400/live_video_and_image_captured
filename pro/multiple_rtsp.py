import cv2
import os
import time
from datetime import datetime

def capture_images_from_rtsp(rtsp_urls, base_folder='images', interval=10):
    # Create the base images folder if it doesn't exist
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    try:
        while True:
            for idx, rtsp_url in enumerate(rtsp_urls, start=1):
                # Create a subfolder for each camera
                camera_folder = os.path.join(base_folder, f"camera{idx}")
                if not os.path.exists(camera_folder):
                    os.makedirs(camera_folder)

                # Initialize the video capture for each RTSP stream
                cap = cv2.VideoCapture(rtsp_url)

                if not cap.isOpened():
                    print(f"Failed to connect to the RTSP stream for camera{idx}.")
                    continue

                # Capture a single frame
                ret, frame = cap.read()

                if ret:
                    # Generate a unique filename based on the current timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_image_path = os.path.join(camera_folder, f"captured_{timestamp}.jpg")
                    
                    # Save the captured image
                    cv2.imwrite(output_image_path, frame)
                    print(f"Image saved for camera{idx} as {output_image_path}")
                else:
                    print(f"Failed to capture an image from the stream for camera{idx}.")

                # Release the stream for this camera
                cap.release()

            # Wait for the specified interval (10 seconds by default)
            time.sleep(interval)

    except KeyboardInterrupt:
        print("Capture stopped by user.")

# Example usage with multiple RTSP URLs
rtsp_urls = [
    "rtsp://192.168.1.5:8080/h264_pcm.sdp",   # Replace with actual RTSP URLs
    "rtsp://192.168.1.14:8080/h264_pcm.sdp"
]
capture_images_from_rtsp(rtsp_urls)
