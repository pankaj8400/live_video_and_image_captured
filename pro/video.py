import cv2
import os
import time
from datetime import datetime

def record_videos_from_rtsp(rtsp_urls, base_folder='videos', duration=60, fps=20, frame_width=640, frame_height=480):
    # Create the base videos folder if it doesn't exist
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
    
    # Set up video writers for each camera
    video_writers = []
    caps = []

    # Initialize video captures and video writers for each RTSP URL
    for idx, rtsp_url in enumerate(rtsp_urls, start=1):
        # Create a subfolder for each camera video file
        camera_folder = os.path.join(base_folder, f"camera{idx}")
        if not os.path.exists(camera_folder):
            os.makedirs(camera_folder)

        # Generate a unique filename based on the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_video_path = os.path.join(camera_folder, f"recording_{timestamp}.mp4")

        # Initialize the video capture
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            print(f"Failed to connect to the RTSP stream for camera{idx}.")
            continue
        caps.append(cap)

        # Initialize the video writer with MP4 format
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
        video_writers.append(video_writer)

        print(f"Recording started for camera{idx}: {output_video_path}")

    # Record for the specified duration (in seconds)
    start_time = time.time()
    try:
        while time.time() - start_time < duration:
            for idx, (cap, video_writer) in enumerate(zip(caps, video_writers), start=1):
                ret, frame = cap.read()
                if ret:
                    # Write the frame to the video file
                    video_writer.write(frame)
                else:
                    print(f"Failed to capture frame for camera{idx}.")

            # Wait briefly to match the FPS (optional sleep to avoid high CPU usage)
            time.sleep(1 / fps)

    except KeyboardInterrupt:
        print("Recording stopped by user.")
    
    finally:
        # Release all video captures and writers
        for cap in caps:
            cap.release()
        for video_writer in video_writers:
            video_writer.release()
        cv2.destroyAllWindows()
        print("All recordings completed.")

# Example usage with multiple RTSP URLs
rtsp_urls = [
    "rtsp://192.168.1.5:8080/h264_pcm.sdp",   # Replace with actual RTSP URLs
    "rtsp://192.168.1.6:8080/h264_pcm.sdp"
]
record_videos_from_rtsp(rtsp_urls)
