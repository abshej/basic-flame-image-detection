import numpy as np
import cv2
import matplotlib.pyplot as plt
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

 
#initialise camera, set parameters and capture buffer
cam = PiCamera()
cam.framerate = 6
cam.resolution = (640, 480)
raw_feed = PiRGBArray(camera, size=(640, 480))
 
#time needed for camera to adapt
time.sleep(0.2) #increase or decrease depending on frame rate

 
# capture frames
for feed in camera.capture_continuous(raw_feed, format="rgb", use_video_port=True):
 frame = feed.array
 
 #median blurring frame
 #frame = cv2.medianBlur(frame, 3)
    
 #ycbcr thresholding
 framey = cv2.cvtColor(frame, cv2.COLOR_RGB2YCR_CB) #rgb to ycrcb conversion     
 lower_y = np.array([230,120,60])
 upper_y = np.array([300,300,300])
 thres_mask_y1 = cv2.inRange(framey, lower_y, upper_y) #obtaining binary
 #bit_mask_y1 = cv2.bitwise_and(framey, framey, mask= thres_mask_y1)         
 lower_y2 = np.array([130,180,30])
 upper_y2 = np.array([230,200,90])
 thres_mask_y2 = cv2.inRange(framey, lower_y2, upper_y2) #obtaining binary
 #bit_mask_y2 = cv2.bitwise_and(framey, framey, mask= thres_mask_y2)
 thres_mask_y = cv2.bitwise_or(thres_mask_y1, thres_mask_y2) #combined mask 
 
 #rgb thresholding
 lower_red1 = np.array([230,150,40])
 upper_red1 = np.array([300,300,270])
 thres_mask_red1 = cv2.inRange(frame, lower_red1, upper_red1)
 #bit_mask_rgb1 = cv2.bitwise_and(frame, frame, mask= thres_mask_red)
 lower_red2 = np.array([200,90,40])
 upper_red2 = np.array([240,120,80])
 thres_mask_red2 = cv2.inRange(frame, lower_red2, upper_red2)
 #bit_mask_rgb2 = cv2.bitwise_and(frame, frame, mask= thres_mask_red) 
 thres_mask_red = cv2.bitwise_or(thres_mask_red1, thres_mask_red2) 
 
 #hsv thresholding
 hsv_edit = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.uint8)
 lower_blue = np.array([4,100,255])
 upper_blue = np.array([70,300,300])
 thres_mask_hsv = cv2.inRange(hsv_edit, lower_blue, upper_blue)
 #bit_mask_hsv = cv2.bitwise_and(frame,frame, mask= thres_mask)
 
 
 #using masks
 thres_mask_hsvnrgb = cv2.bitwise_or(thres_mask_hsv, thres_mask_red)
 bit_mask_three = cv2.bitwise_and(thres_mask_hsvnrgb, thres_mask_y)
 
 
 #decision making regarding detection
 n = cv2.countNonZero(bit_mask_three)
 c = 0
 if float(n)/float(frame.size) > 0.0005: #need to change
   cv2.imshow('Flame Detected', bit_mask_three)
   key = cv2.waitKey(1) & 0xFF
 
 else: 
   cv2.imshow('Not Detected', frame)
   key = cv2.waitKey(1) & 0xFF
 

 rawCapture.truncate(0) #clear buffer for next frame !IMPORTANT!
 
 # if the `q` key was pressed, break from the loop
 if key == ord("q"):
    break

cv2.destroyAllWindows() 


