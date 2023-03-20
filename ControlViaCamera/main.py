"""
Author: Haowei Li
Date: 2023-03-19

Overview:
This is the main file for running the camera control system.
"""

import cv2 #OpenCV Module
import time
import mediapipe as mp #Hand Tracking Module

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0
backSub = cv2.createBackgroundSubtractorKNN(history=200)

while True:
    success, frame = cap.read()                                                           # Read the image from the camera
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)                                       # Convert the image to RGB
    results = hands.process(frameRGB)                                                     # Process the image


    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:                                    # Loop through all the hands
            for id, lm in enumerate(handLms.landmark):                                  # Loop through all the landmarks
                h, w, c = frame.shape                                                     # Get the height, width and channel of the image
                cx, cy = int(lm.x *w), int(lm.y*h)                                      # Get the x and y coordinates of the landmark
                cv2.putText(frame,str(id), (cx,cy),                                       # Display the index of the landmark
                            cv2.FONT_HERSHEY_PLAIN, 1, (255,0,255), 1) 
                cv2.circle(frame, (cx,cy), 3, (255,0,255), cv2.FILLED)                    # Draw a circle on the landmark
            """Calculates the distance between two landmarks: 4 and 8"""
            x1, y1 = handLms.landmark[4].x*w, handLms.landmark[4].y*h                   # Get the x and y coordinates of the landmark 4
            x2, y2 = handLms.landmark[8].x*w, handLms.landmark[8].y*h                   # Get the x and y coordinates of the landmark 8
            length = ((x2-x1)**2 + (y2-y1)**2)**0.5                                     # Calculate the distance between the two landmarks
            print(length)                                                               # Print the distance
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)               # Draw the connections between the landmarks


    """FPS Calculation"""
    cTime = time.time()                                                                 # Get the current time                               
    fps = 1/(cTime-pTime)                                                               # Calculate the fps
    pTime = cTime                                                                       # Set the previous time to the current time
    """Open Source Computer Vision Display"""
    cv2.putText(frame,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)  # Display the fps on the image

    cv2.imshow("Image", frame)                                                            # Display the image
    cv2.waitKey(1)                                                                      # Wait for 1ms                

    if cv2.waitKey(1) & 0xFF == ord('q'):                                               # If the user presses q, then quit windows
        break