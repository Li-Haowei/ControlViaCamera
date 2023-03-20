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

largest = 0
smallest = 0
while True:
    success, frame = cap.read()                                                             # Read the image from the camera
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)                                       # Convert the image to RGB
    results = hands.process(frameRGB)                                                       # Process the image

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:                                        # Loop through all the hands
            for id, lm in enumerate(handLms.landmark):                                      # Loop through all the landmarks
                h, w, c = frame.shape                                                       # Get the height, width and channel of the image
                cx, cy = int(lm.x *w), int(lm.y*h)                                          # Get the x and y coordinates of the landmark
                cv2.putText(frame,str(id), (cx,cy),                                         # Display the index of the landmark
                            cv2.FONT_HERSHEY_PLAIN, 1, (255,0,255), 1) 
                cv2.circle(frame, (cx,cy), 3, (255,0,255), cv2.FILLED)                      # Draw a circle on the landmark
            """Calculate the angle between landmarks (0,4) and (0,8)"""
            x1, y1 = handLms.landmark[4].x*w, handLms.landmark[4].y*h                       # Get the x and y coordinates of landmark 4
            x2, y2 = handLms.landmark[8].x*w, handLms.landmark[8].y*h                       # Get the x and y coordinates of landmark 8
            x0, y0 = handLms.landmark[0].x*w, handLms.landmark[0].y*h                       # Get the x and y coordinates of landmark 0
            angle = int(((x2-x1)*(x0-x1)+(y2-y1)*(y0-y1))/((x2-x1)**2+(y2-y1)**2)**0.5)     # Calculate the angle
            if angle > largest:                                                             # Get the largest and smallest angle                         
                largest = angle
            if angle < smallest:
                smallest = angle
            angle = (angle-smallest)/(largest-smallest)*100
            print("angle: ", angle)


            """Draw red line between landmarks 0 and 4, and 0 and 8"""
            cv2.line(frame, (int(x0),int(y0)), (int(x2),int(y2)), (0,0,255), 3)             # Draw a red line between landmark 0 and 8
            cv2.line(frame, (int(x0),int(y0)), (int(x1),int(y1)), (0,0,255), 3)             # Draw a red line between landmark 0 and 4

            """Display the angle on the top right corner"""
            cv2.putText(frame,str(angle), (w-100,50), 
                        cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)                          # Display the angle on the image
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)                 # Draw the landmarks and connections

            """Display a volumn bar on the top left corner"""
            cv2.rectangle(frame, (50,50), (85,150), (0,255,0), 3)                           # Draw a rectangle
            cv2.rectangle(frame, (50,150), (85,150-int(angle*1.5)), (0,255,0), cv2.FILLED)  # Draw a rectangle



            






    """FPS Calculation"""
    cTime = time.time()                                                                     # Get the current time                               
    fps = 1/(cTime-pTime)                                                                   # Calculate the fps
    pTime = cTime                                                                           # Set the previous time to the current time
    """Open Source Computer Vision Display"""
    cv2.putText(frame,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)    # Display the fps on the image

    cv2.imshow("Image", frame)                                                              # Display the image
    cv2.waitKey(1)                                                                          # Wait for 1ms                

    if (cv2.waitKey(1) & 0xFF == ord('q') 
        or 
        cv2.getWindowProperty('Image',cv2.WND_PROP_VISIBLE) < 1):                           # Quit windows
        break