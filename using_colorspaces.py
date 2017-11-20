#author: Avadhoot S
"""
program for detecting flames in image frames
using three colorspace thresholding
threshold values obtained using experimentation and are not universal
adaptive thresholding is suggested for eliminating false positives
"""
import cv2 #opencv2
import numpy as np
import matplotlib.pyplot as plt
import sys 

frame = cv2.cvtColor(cv2.imread(str(sys.argv[1]), -1), cv2.COLOR_BGR2RGB) #standard bgr converted to rgb beforehand
#framegr = cv2.imread(str(sys.argv[1]), 0) #grayscale frame

#median blurring frame
#frame = cv2.medianBlur(frame, 3)
    
#ycbcr thresholding
framey = cv2.cvtColor(frame, cv2.COLOR_RGB2YCR_CB) #rgb to ycbcr conversion

lower_y = np.array([230,120,60])
upper_y = np.array([300,300,150])
thres_mask_y1 = cv2.inRange(framey, lower_y, upper_y) #obtaining binary
bit_mask_y1 = cv2.bitwise_and(framey, framey, mask= thres_mask_y1) 

lower_y2 = np.array([170,180,30])
upper_y2 = np.array([230,200,80])
thres_mask_y2 = cv2.inRange(framey, lower_y2, upper_y2) #obtaining binary
#bit_mask_y2 = cv2.bitwise_and(framey, framey, mask= thres_mask_y2)

thres_mask_y = cv2.bitwise_or(thres_mask_y1, thres_mask_y2) #combining both results 

#obtaining masked image

#rgb thresholding
lower_red1 = np.array([230,150,40])
upper_red1 = np.array([300,300,150])
thres_mask_red1 = cv2.inRange(frame, lower_red1, upper_red1)
#bit_mask_rgb1 = cv2.bitwise_and(frame, frame, mask= thres_mask_red)

lower_red2 = np.array([200,90,40])
upper_red2 = np.array([240,120,80])
thres_mask_red2 = cv2.inRange(frame, lower_red2, upper_red2)
#bit_mask_rgb2 = cv2.bitwise_and(frame, frame, mask= thres_mask_red)

thres_mask_red = cv2.bitwise_or(thres_mask_red1, thres_mask_red2) #combining both results


#hsv thresholding
hsv_edit = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.uint8) 

lower_blue = np.array([4,100,255])
upper_blue = np.array([70,300,300])
thres_mask_hsv = cv2.inRange(hsv_edit, lower_blue, upper_blue)
#bit_mask_hsv = cv2.bitwise_and(frame,frame, mask= thres_mask)

#bitwise condition
thres_mask_hsvnrgb = cv2.bitwise_or(thres_mask_hsv, thres_mask_red)
bit_mask_three = cv2.bitwise_and(thres_mask_hsvnrgb, thres_mask_y)

#decision making regarding detection
n = cv2.countNonZero(bit_mask_three)
c = 0
if float(n)/float(frame.size) > 0.0005: #need to change
   c = 1

#displaying results
plt.subplot(121), plt.imshow(frame)
plt.title('original frame'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(bit_mask_three)
plt.title('resulting frame'), plt.xticks([]), plt.yticks([])
if c==1:
    plt.figtext(.02, .02, "FLAME DETECTED\n", style='italic', bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
else:
    plt.figtext(.02, .02, "FLAME NOT DETECTED\n", style='italic', bbox={'facecolor':'green', 'alpha':0.5, 'pad':10})

plt.show()

