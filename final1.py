import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)# import the necessary packages
import os,sys
import sys
import termios
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np


#Camera Servos
GPIO.setup(13,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
upDownServo = GPIO.PWM(13,50)
baseServo = GPIO.PWM(19,50)
x = 7
y = 4
baseServo.start(x)
upDownServo.start(y)
time.sleep(1)
def nothing(x):
    pass
# Creating a windows for later use
cv2.namedWindow('HueComp')
cv2.namedWindow('SatComp')
cv2.namedWindow('ValComp')

# Creating track bar for min and max for hue, saturation and value
# You can adjust the defaults as you like
cv2.createTrackbar('hmin', 'HueComp',12,179,nothing)
cv2.createTrackbar('hmax', 'HueComp',37,179,nothing)

cv2.createTrackbar('smin', 'SatComp',96,255,nothing)
cv2.createTrackbar('smax', 'SatComp',255,255,nothing)

cv2.createTrackbar('vmin', 'ValComp',186,255,nothing)
cv2.createTrackbar('vmax', 'ValComp',255,255,nothing)



def forward():
	GPIO.setup(7,GPIO.LOW)
	GPIO.setup(11,GPIO.LOW)
def stop():
	GPIO.setup(7,GPIO.HIGH)
	GPIO.setup(11,GPIO.HIGH)
def left():
	GPIO.setup(7,GPIO.LOW)
	GPIO.setup(11,GPIO.HIGH)
def right():
	GPIO.setup(7,GPIO.HIGH)
	GPIO.setup(11,GPIO.LOW)





# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 50


rawCapture = PiRGBArray(camera, size=(320, 240))

# allow the camera to warmup
time.sleep(0.1)
avgArea = 0
avgI = 0
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp

	# and occupied/unoccupied text
        image = frame.array
        hmn = cv2.getTrackbarPos('hmin','HueComp')
        hmx = cv2.getTrackbarPos('hmax','HueComp')


    	smn = cv2.getTrackbarPos('smin','SatComp')
    	smx = cv2.getTrackbarPos('smax','SatComp')


    	vmn = cv2.getTrackbarPos('vmin','ValComp')
    	vmx = cv2.getTrackbarPos('vmax','ValComp')
        # b,g,r = frame.T

        blur = cv2.blur(image, (3,3))

        #hsv to complicate things, or stick with BGR
        hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
        # print(hsv)
        #thresh = cv2.inRange(hsv,np.array((0, 200, 200)), np.array((20, 255, 255)))

        #upper = np.array([225,88,50], dtype="uint8")


		# lower = np.array([57,254,20], dtype="uint8")
        # upper = np.array([60,255,35],dtype="uint8")
        lower = np.array([54,255,21], dtype="uint8")
        upper = np.array([67,255,38],dtype="uint8")


	#lower = np.array([76,31,4],dtype="uint8")
        #upper = np.array([225,88,50], dtype="uint8")
        #upper = np.array([210,90,70], dtype="uint8")
        # 54,255,21
        # 67, 255, 38
        thresh = cv2.inRange(hsv, lower, upper)
        thresh2 = thresh.copy()

        # find contours in the threshold image
        contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)



        # finding contour with maximum area and store it as best_cnt
        max_area = 0
        best_cnt = 1
        for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > max_area:
                        max_area = area
                        best_cnt = cnt

        if avgI < 1:
            avgI = avgI + 1;
            avgArea = avgArea + max_area;
        else:
            avgI = 0;
            max_area = avgArea/3;
            avgArea = 0
            # finding centroids of best_cnt and draw a circle there
            M = cv2.moments(best_cnt)
            cy,cx = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            #if best_cnt>1:

            cv2.circle(blur,(cx,cy),10,(0,0,255),-1)
            # show the frame
            cv2.imshow("Frame", blur)
            cv2.imshow('thresh',thresh2)
            # if cx not in range(250,330):
                # if (cx-270) > 0:
                #     #E
                # else:
                    #R
            if max_area > 450:
                if (cx-200) > 0:
                    key = "e1"
                else:
                    key = "r1"

                if key == 'r':
            		if x < 12:
            		    x = x + 0.5
            		    baseServo.ChangeDutyCycle(x)
            		    time.sleep(0.2)
                if key == 'e':
            	    if x > 4:
            		    x = x - 0.5
            		    baseServo.ChangeDutyCycle(x)
            		    time.sleep(0.2)
		if (cy-250) > 0:
			key = "f1"
		else:
			key = "v1"
                if key == 'v':
            	    if y < 8:
            		    y = y + 0.5
            		    upDownServo.ChangeDutyCycle(y)
            		    time.sleep(0.2)
                if key == 'f':
            	    if y > 1:
            		    y = y - 0.5
            		    upDownServo.ChangeDutyCycle(y)
            		    time.sleep(0.2)
            print("cx " +str(cx) + " cy " + str(cy))
            print("Area " + str(max_area))
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
        rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
        	break
