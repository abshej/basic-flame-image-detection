import numpy as np
import cv2
import matplotlib.pyplot as plt
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 6
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)

 
# capture frames from the camera
for frames in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
 # grab the raw NumPy array representing the image, then initialize the timestamp
 # and occupied/unoccupied text
 frame = frames.array
 
 # show the frame
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

 thres_mask_y = cv2.bitwise_or(thres_mask_y1, thres_mask_y2)  
 #obtaining masked image 
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
 #mask
 thres_mask_hsvnrgb = cv2.bitwise_or(thres_mask_hsv, thres_mask_red)
 bit_mask_three = cv2.bitwise_and(thres_mask_hsvnrgb, thres_mask_y)
 flame_frame = cv2.bitwise_and(frame, frame, mask=bit_mask_three)
 print bit_mask_three
 #decision making regarding detection
 n = cv2.countNonZero(bit_mask_three)
 c = 0
 if float(n)/float(frame.size) > 0.0005: #need to change
   cv2.imshow('frame', flame_frame)
   key = cv2.waitKey(1) & 0xFF
 
 else: 
   cv2.imshow('frame', frame)
   key = cv2.waitKey(1) & 0xFF
 


 # clear the stream in preparation for the next frame
 rawCapture.truncate(0)
  # if the `q` key was pressed, break from the loop
 if key == ord("q"):
    break

cv2.destroyAllWindows()


