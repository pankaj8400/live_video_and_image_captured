import cv2
import os
import time
from datetime import datetime

def capture_image_from_rtsp(rtsp_url, folder_path='images', interval=10):
    # Create the images folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    try:
        while True:
            # Reinitialize the video capture in each iteration
            cap = cv2.VideoCapture(rtsp_url)
            
            if not cap.isOpened():
                print("Failed to connect to the RTSP stream.")
                return

            # Capture a single frame
            ret, frame = cap.read()
            
            if ret:
                # Generate a unique filename based on the current timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_image_path = os.path.join(folder_path, f"captured_{timestamp}.jpg")
                
                # Save the captured image
                cv2.imwrite(output_image_path, frame)
                print(f"Image saved as {output_image_path}")
            else:
                print("Failed to capture an image from the stream.")
            
            # Release the stream
            cap.release()
            
            # Wait for the specified interval (10 seconds by default)
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("Capture stopped by user.")

# Example usage
rtsp_url = "rtsp://192.168.1.5:8080/h264_pcm.sdp"
capture_image_from_rtsp(rtsp_url)
