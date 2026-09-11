import asyncio
import cv2 
import numpy as np
from mavsdk import OffboardError,VelocityBodyYawspeed

current_state = {
    'delta_x' : 0.0, 
    'delta_y' : 0.0,
    'is_running' : True,
    'target_found' : False
}


def compute_commands(e_x, e_y, kp_yaw = 0.094, kp_alt = 0.0021):
    #Define constraints
    deadband_px = 15.0
    max_yaw_rate = 30.0
    max_vert_vel = 0.5
    # Applyinh deadband
    if abs(e_x) < deadband_px:
        e_x = 0 
    if abs(e_y) < deadband_px:
        e_y = 0 

    #Now apply the control relationship, open cv defines +y as negative hence the -. 
    raw_yaw_cmd = kp_yaw * e_x
    raw_alt_cmd = -kp_alt * e_y

    # Apply saturation clamps

    yaw_rate = max(-max_yaw_rate, min(max_yaw_rate, raw_yaw_cmd))
    vz_cmd = max(-max_vert_vel, min(max_vert_vel, raw_alt_cmd))

    return yaw_rate, vz_cmd

async def vision_loop():
    cap = cv2.VideoCapture(0) # Initialize camera feed 
    while current_state['is_running']:

        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        height, width, _ = frame.shape
        centre_x = width // 2
        centre_y = height //2

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #convert to hsv format
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

        contours, _= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
                current_state['delta_x'] = delta_x
                current_state['delta_y'] = delta_y
                current_state['target_found'] = True
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (target_x, target_y), 5, (0, 0, 255), -1)
            else:
                current_state["target_found"] = False
                current_state["delta_x"] = 0.0
                current_state["delta_y"] = 0.0
        else:
            current_state["target_found"] = False
            current_state["delta_x"] = 0.0
            current_state["delta_y"] = 0.0

        cv2.drawMarker(
            frame,
            (centre_x, centre_y),
            (255, 255, 255),
            markerType=cv2.MARKER_CROSS,
            markerSize=20,
            thickness=2,)
        cv2.imshow("Drone Visual Tracker", frame)

        # Check for exit key 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("User requested exit.")
            current_state["is_running"] = False
            break

        # Yield execution back to the asyncio event loop for other tasks
        await asyncio.sleep(0.001)

    # 3. Clean up hardware resources on loop termination
    cap.release()
    cv2.destroyAllWindows()

            
        
        
                



    