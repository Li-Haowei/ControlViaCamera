"""
Author: Haowei Li
Date: 2023-03-19

Overview:
This is the main file for running the camera control system.
"""

import numpy as np
import cv2 as cv

# initialize last frame
last_frame = None

# initialize camera
cap = cv.VideoCapture(0)

# check if camera is opened
if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    
    # Display the resulting frame
    cv.imshow('Control', frame)
    cv.imshow('Gray', gray)
    if cv.waitKey(1) == ord('q'):
        break

    # compare last frame with current frame, display the difference on a new window with black and white
    if last_frame is not None:
        diff = cv.absdiff(last_frame, frame)
        cv.imshow('Motion Tracking', diff)


    # save current frame as last frame
    last_frame = frame

    

# When everything done, release the captureq
cap.release()
cv.destroyAllWindows()