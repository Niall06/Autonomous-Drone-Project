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

        # To make the image more clear morphological dilation is used
        mask = cv2.dilate(mask, None, iterations=2)

        # Find contours in the mask
        contours, _= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Next, crosshairs are drawn at the centre
        cv2.drawMarker(frame, (centre_x, centre_y), (255, 255, 255), cv2.MARKER_CROSS, markerSize=20, thickness=2)

        # The largest contor is selected, (biggest blob)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)

            #Filter out small contours based on their area
            if cv2.contourArea(largest_contour)> 500:
                # Now draw bounding box around the largest blob
                x, y, w, h = cv2.boundingRect(largest_contour)
                #and find drone target position
                

                target_x = x + w //2 
                target_y = y + h //2

                # Pixel displacement error

                delta_x = target_x - centre_x
                delta_y = target_y - centre_y

                cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
                cv2.circle(frame, (target_x, target_y), 5, (0,255,0), -1)

                # Line from centre to target
                cv2.line(frame, (centre_x, centre_y), (target_x, target_y), (255, 0, 0), 2)
                



