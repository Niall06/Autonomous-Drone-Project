import cv2 
import numpy as np 

def main():
    # Initialize the webcam feed
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    print("Webcam feed started. Press 'q' to exit.")
    # Loop to continuously get frames from the webcam
    # The q means that the loop will break when the 'q' key is pressed

    while True:
        ret, frame = cap.read()
        # ret is a boolean that returns true or false based on whether there was a frame recorded. 
        # Check if the frame was captured successfully
        if not ret:
            print("Error: Could not read frame.")
            break
        height, width, _ = frame.shape
        centre_x = width // 2
        centre_y = height //2

        # Convert to HSV colour space
        # This stands for Hue, Saturation, and Value. It is a cylindrical color space that is often used in computer vision applications because it separates color information (hue) from intensity information (value).
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2HSV)

        # Next must define what constitutes the colour red
        # It must be defined by two ranges as red sits at 0 degrees on the hue spectrum.

        lower_red1 = np.array([0,120 , 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        mask = mask1 + mask2
        # This creates a boolean mask for the specified red pixels that the drone will track. 

        
    