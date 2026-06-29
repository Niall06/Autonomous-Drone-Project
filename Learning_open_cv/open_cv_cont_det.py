import cv2 as cv
import numpy as np
#this is how to identify contours in an image using OpenCV

img = cv.imread('Learning_open_cv/Photos/Cat.jpg')
cv.imshow('Cat', img)

blank = np.zeros(img.shape, dtype='uint8')
cv.imshow('Blank', blank)




gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#This converts the initial image of the cat to grayscale.


cv.imshow('Gray', gray)

canny= cv.Canny(img, 125, 175)
#This applies the Canny edge detection algorithm to the original image. The first argument is the input image, and the second and third arguments are the lower and upper thresholds for the hysteresis procedure in the Canny algorithm. The output is a binary image where edges are highlighted.
cv.imshow('Canny edges', canny )


blur = cv.GaussianBlur(gray, (7,7), cv.BORDER_DEFAULT)
#This applies a Gaussian blur to the grayscale image. The first argument is the input image, the second argument is the size of the kernel (in this case, a 7x7 kernel), and the third argument specifies the border type. The Gaussian blur helps to reduce noise and detail in the image, which can improve edge detection.
cv.imshow('Blur', blur)

canny2 = cv.Canny(blur, 125, 175)
cv.imshow('Canny edges after blur', canny2)
#Now must use the find contors function to finf the contours of the image. 

contours, hieraches = cv.findContours(canny2, cv.RETR_LIST, cv.CHAIN_APPROX_NONE) 
#This function fins the contoutrs of a binary image. Then it returns a list of contours and a hierarchy of the contours. The first argument is the input image, which should be a binary image (like the output of the Canny edge detector). The second argument specifies the contour retrieval mode (cv.RETR_LIST retrieves all contours without establishing any hierarchical relationships). The third argument specifies the contour approximation method (cv.CHAIN_APPROX_NONE stores all the points of the contours).
print(f'{len(contours)} contours found!')

#
# Bluring the image significanlty reduces the number of contours found. 
cv.drawContours(blank, contours, -1, (0,0,255), 1)
cv.imshow('Contours Drawn', blank)
#This function draws contours on an image. The first argument is the image on which to draw. 
# For thresholidng, it binarises an image based on a threshold value. Pixels with intensity values above the threshold are set to the maximum value (white), and those below are set to the minimum value (black). This can help in isolating objects in an image for contour detection.
# If you then try and find the contours of the thresholded image, you will find that it is much easier to identify the contours of the objects in the image.


cv.waitKey(0)