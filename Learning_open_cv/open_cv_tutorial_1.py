#                       BASICS

import cv2 as cv
img =cv.imread('Learning_open_cv/Photos/Cat.jpg')
#This function reads an image from a file and returns it as a NumPy array. The image can be in color or grayscale, depending on the flags used.


cv.imshow('Cat', img)
#This function displays an image in a window. The first argument is the name of the window, and the second argument is the image to be displayed. The window will remain open until a key is pressed.

cv.waitKey(0)
#This function waits for a key event indefinitely (when 0 is passed as an argument). If a positive integer is passed, it will wait for that many milliseconds. If a key is pressed during the wait, the function will return the ASCII value of the key.


# Reading Videos

cap = cv.VideoCapture('Learning_open_cv/Videos/dog.mp4')
#This function creates a VideoCapture object, which allows you to read video files or capture video from a camera. The argument can be a filename (for video files) or an integer (for camera devices).

while True:
    IsTrue, frame = cap.read()
    #This function reads a frame from the video capture object. It returns a boolean indicating whether the read was successful and the frame itself.
    cv.imshow('Video', frame)

    if cv.waitKey(20) & 0xFF==ord('d'):
        # Break the loop if 'd' is pressed
        break
cap.release()
cv.destroyAllWindows()
#These lines release the video capture object and close all OpenCV windows. It's important to release resources when they are no longer needed to avoid memory leaks and other issues.