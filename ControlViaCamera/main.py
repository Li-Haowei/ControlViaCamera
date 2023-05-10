"""
Author: Haowei Li
Date: 2023-03-19

Overview:
This is the main file for running the camera control system.
"""

import cv2 #OpenCV Module
import time
import mediapipe as mp #Hand Tracking Module
from pynput.keyboard import Key,Controller #Keyboard Module


class HandControl():
    def __init__(self, default_camera = 0):
        """
        initialize everything needed to run this program, and selecting the desired camera to work with
        """
        try:
            self.cap = cv2.VideoCapture(default_camera)
        except:
            print("Camera not found")
            exit()
        else:
            print("Camera found")
        try:
            self.keyboard = Controller()
        except:
            print("Keyboard not found")
            exit()
        else:
            print("Keyboard found")

        try:
            self.mpHands = mp.solutions.hands
        except:
            print("Hand tracking module not found")
            exit()
        else:
            self.hands = self.mpHands.Hands(static_image_mode=False,
                                max_num_hands=2,
                                min_detection_confidence=0.5,
                                min_tracking_confidence=0.5)
            self.mpDraw = mp.solutions.drawing_utils
        self.pTime = 0
        self.cTime = 0
        self.angle = 0
        self.largest = 1
        self.smallest = 0
        self.fps = 0
    
    def setLargest(self, num):
        """
        Set the largest angle
        """
        self.largest = num
    def setSmallest(self, num):
        """
        Set the smallest angle
        """
        self.smallest = num
    def setAngle(self, num):
        """
        Set the angle
        """
        self.angle = num
    def setPTime(self, num):
        """
        Set the previous time
        """
        self.pTime = num
    def setCTime(self, num):
        """
        Set the current time
        """
        self.cTime = num

    def setFPS(self, num):
        """
        Set the fps
        """
        self.fps = num


    def calculate_angle(self, x1, y1, x2, y2, x0, y0):
        """
        Calculates angle between three joints
        """
        return int(((x2-x1)*(x0-x1)+(y2-y1)*(y0-y1))/((x2-x1)**2+(y2-y1)**2)**0.5)             # Calculate the angle

    def volume_control(self, num):
        """
        if num > 50, increase, else decrease the volume
        """
        if num > 50:
            self.keyboard.press(Key.media_volume_up)
            self.keyboard.release(Key.media_volume_up)
            time.sleep(0.1)
            self.keyboard.press(Key.media_volume_down)
            self.keyboard.release(Key.media_volume_down)
        elif num < 50:
            self.keyboard.press(Key.media_volume_down)
            self.keyboard.release(Key.media_volume_down)
            time.sleep(0.1)
            self.keyboard.press(Key.media_volume_up)
            self.keyboard.release(Key.media_volume_up)

    def get_coordinates(self, x, y, w, h):
        """
        Get the x and y coordinates of the landmark
        """
        x1, y1 = x*w, y*h
        return x1, y1

    def degree_to_volume(self):
        """
        Convert the angle to volume
        """
        volume = (self.angle-self.smallest)/(self.largest-self.smallest)*100
        return volume

    def draw_volume_bar(self, x0, y0, x1, y1, x2, y2, frame, w):
        """
        given the angle, draw the volume bar
        """
        """FPS Calculation"""
        self.cTime = time.time()                                                                     # Get the current time                               
        fps = self.calculateFPS()                                                                   # Calculate the fps
        self.pTime = self.cTime                                                                           # Set the previous time to the current time
        """Open Source Computer Vision Display"""
        cv2.putText(frame,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)    # Display the fps on the image
        """Draw red line between landmarks 0 and 4, and 0 and 8"""
        cv2.line(frame, (int(x0),int(y0)), (int(x2),int(y2)), (0,0,255), 3)             # Draw a red line between landmark 0 and 8
        cv2.line(frame, (int(x0),int(y0)), (int(x1),int(y1)), (0,0,255), 3)             # Draw a red line between landmark 0 and 4

        """Display the angle on the top right corner"""
        cv2.putText(frame,str(self.angle), (w-100,50), 
                                cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)                          # Display the angle on the image
        self.mpDraw.draw_landmarks(frame, self.handLms, self.mpHands.HAND_CONNECTIONS)                 # Draw the landmarks and connections

        """Display a volumn bar on the top left corner"""
        cv2.rectangle(frame, (50,150), (85,50), (255, 0 ,255), 3)                       # Draw a rectangle                    
        cv2.rectangle(frame, (50,150), (85,150-int(self.angle*1.5)), (0,255,0), cv2.FILLED)  # Draw a rectangle


    def setHand(self, handLms):
        """
        Set the hand
        """
        self.handLms = handLms

    def drawHand(self, frame, id, cx, cy):
        cv2.putText(frame,str(id), (cx,cy),                                         # Display the index of the landmark
                                    cv2.FONT_HERSHEY_PLAIN, 1, (255,0,255), 1) 
        cv2.circle(frame, (cx,cy), 3, (255,0,255), cv2.FILLED)                      # Draw a circle on the landmark

    def calculateFPS(self):
        if self.cTime-self.pTime != 0:
            self.setFPS(1/(self.cTime-self.pTime))                                                                   # Calculate the fps
            return self.fps
        else:
            return 0
        
    def unit_test_1(self):
        """
        Test the get_coordinates function
        """
        x, y = self.get_coordinates(0.5, 0.5, 100, 100)
        assert x == 50
        assert y == 50
        print("Unit Test 1 Passed")
    
    def unit_test_2(self):
        """
        Test the calculate_angle function
        """
        angle = self.calculate_angle(0, 0, 1, 1, 0, 1)
        assert angle == 0
        print("Unit Test 2 Passed")

    def unit_test_3(self):
        """
        Test the volume_control function
        """
        self.volume_control(51)
        print("Unit Test 3 Passed")

    def unit_test_4(self):
        """
        Test the setHand function
        """
        self.setHand(1)
        assert self.handLms == 1
        print("Unit Test 4 Passed")

    def run_all_unit_tests(self):
        """
        Run all the unit tests
        """
        self.unit_test_1()
        self.unit_test_2()
        self.unit_test_3()
        self.unit_test_4()
    
    def run(self):
        """
        Run the program
        """
        while True:
            try:
                success, frame = self.cap.read()                                                         # Read the image from the camera
            except:
                print("Camera mulfunction")
                exit()
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)                                       # Convert the image to RGB
            results = self.hands.process(frameRGB)                                                       # Process the image

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:                                        # Loop through all the hands
                    self.setHand(handLms)
                    for id, lm in enumerate(handLms.landmark):                                      # Loop through all the landmarks
                        h, w, c = frame.shape                                                       # Get the height, width and channel of the image
                        cx, cy = int(lm.x *w), int(lm.y*h)                                          # Get the x and y coordinates of the landmark
                        self.drawHand(frame, id, cx, cy)                                            # Draw the hand
                    
                    """Calculate the angle between landmarks (0,4) and (0,8)"""
                    x1, y1 = self.get_coordinates(handLms.landmark[4].x, handLms.landmark[4].y, w, h)    # Get the x and y coordinates of landmark 4
                    x2, y2 = self.get_coordinates(handLms.landmark[8].x, handLms.landmark[8].y, w, h)    # Get the x and y coordinates of landmark 8
                    x0, y0 = self.get_coordinates(handLms.landmark[0].x, handLms.landmark[0].y, w, h)    # Get the x and y coordinates of landmark 0
                    self.setAngle(int(((x2-x1)*(x0-x1)+(y2-y1)*(y0-y1))/((x2-x1)**2+(y2-y1)**2)**0.5))     # Calculate the angle
                    
                    if self.angle > self.largest:                                                             # Get the largest and smallest angle                         
                        self.setLargest(self.angle)
                    if self.angle < self.smallest:
                        self.setSmallest(self.angle)
                    self.setAngle(self.degree_to_volume())                               # Convert the angle to volume
                                                                                                    # Control actual system audio volume based on angle
                    try:
                        if self.angle > 0 and self.angle < 100:
                            if self.angle > 50:
                                self.keyboard.press(Key.media_volume_up)
                                self.keyboard.release(Key.media_volume_up)
                            elif self.angle < 50:
                                self.keyboard.press(Key.media_volume_down)
                                self.keyboard.release(Key.media_volume_down)
                    except:
                        print("Volume control mulfunction")
                        exit()
                    else:
                        try:
                            time.sleep(0.1)
                        except:
                            print("Time module mulfunction")
                            exit()

                self.draw_volume_bar(x0, y0, x1, y1, x2, y2, frame, w)                           # Draw the volume bar
            else:
                """FPS Calculation"""
                self.cTime = time.time()                                                                     # Get the current time                               
                fps = self.calculateFPS()                                                                   # Calculate the fps
                self.pTime = self.cTime                                                                           # Set the previous time to the current time
                """Open Source Computer Vision Display"""
                cv2.putText(frame,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)    # Display the fps on the image

            cv2.imshow("Image", frame)                                                              # Display the image
            cv2.waitKey(1)                                                                          # Wait for 1ms                                                                                 # Set the previous angle to the current angle                     
            if (cv2.waitKey(1) & 0xFF == ord('q') 
                or 
                cv2.getWindowProperty('Image',cv2.WND_PROP_VISIBLE) < 1):                           # Quit windows
                break


if __name__ == "__main__":
    HandControl().run_all_unit_tests()
    HandControl().run()
