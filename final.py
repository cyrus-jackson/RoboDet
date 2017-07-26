# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 50
camera.hflip = True

rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)
avgArea = 0
avgI = 0
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
        image = frame.array
        # b,g,r = frame.T

        blur = cv2.blur(image, (3,3))

        #hsv to complicate things, or stick with BGR
        hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
        # print(hsv)
        #thresh = cv2.inRange(hsv,np.array((0, 200, 200)), np.array((20, 255, 255)))

        #upper = np.array([225,88,50], dtype="uint8")
        lower = np.array([60,250,10], dtype="uint8")
        upper = np.array([65,255,200],dtype="uint8")
        thresh = cv2.inRange(hsv, lower, upper)
        thresh2 = thresh.copy()

        # find contours in the threshold image
        contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)



        # finding contour with maximum area and store it as best_cnt
        max_area = 0
        best_cnt = 1
        for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > max_area:
                        max_area = area
                        best_cnt = cnt

        if avgI < 3:
            avgI = avgI + 1;
            avgArea = avgArea + max_area;
        else:
            avgI = 0;
            max_area = avgArea/3;
            avgArea = 0
            # finding centroids of best_cnt and draw a circle there
            M = cv2.moments(best_cnt)
            cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            #if best_cnt>1:

            if cx not in range(250,350):
                if cy not in range(150,220):
                    
            cv2.circle(blur,(cx,cy),10,(0,0,255),-1)
            # show the frame
            #cv2.imshow("Frame", blur)
            #cv2.imshow('thresh',thresh2)
            print("cx " +str(cx) + " cy " + str(cy))
            print("Area " + str(max_area))
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
        rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
        	break
