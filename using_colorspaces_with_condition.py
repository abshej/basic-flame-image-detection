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

median blurring frame
frame = cv2.medianBlur(frame, 2)
    
#ycrcb thresholding
framey = cv2.cvtColor(frame, cv2.COLOR_RGB2YCR_CB) #rgb to ycrcb conversion

lower_y = np.array([230,120,60])
upper_y = np.array([300,300,100])
thres_mask_y1 = cv2.inRange(framey, lower_y, upper_y) #obtaining binary
#bit_mask_y1 = cv2.bitwise_and(framey, framey, mask= thres_mask_y1) 

lower_y2 = np.array([130,180,30])
upper_y2 = np.array([230,200,150])
thres_mask_y2 = cv2.inRange(framey, lower_y2, upper_y2) #obtaining binary
#bit_mask_y2 = cv2.bitwise_and(framey, framey, mask= thres_mask_y2)

thres_mask_y = cv2.bitwise_or(thres_mask_y1, thres_mask_y2) 
id_ycr = (framey[:, :, 0] > framey[:, :, 1]) # y > cr
id_crcb = (framey[:, :, 1] > framey[:, :, 2]) # cr > cb
id_ycb = (framey[:, :, 0] > framey[:, :, 2]) # y > cb
id_ycrcb_ = np.bitwise_and(id_ycr, id_crcb) 
id_ycrcb = np.bitwise_and(id_ycrcb_, id_ycb)

thres_mask_y[id_ycrcb == 0] = [0] #obtaining masked image

#rgb thresholding
lower_red1 = np.array([230,200,40])
upper_red1 = np.array([255,255,255])
thres_mask_red1 = cv2.inRange(frame, lower_red1, upper_red1)
#bit_mask_rgb1 = cv2.bitwise_and(frame, frame, mask= thres_mask_red)

lower_red2 = np.array([200,90,40])
upper_red2 = np.array([240,120,80])
thres_mask_red2 = cv2.inRange(frame, lower_red2, upper_red2)
#bit_mask_rgb2 = cv2.bitwise_and(frame, frame, mask= thres_mask_red)

thres_mask_red = cv2.bitwise_or(thres_mask_red1, thres_mask_red2)
id_rg = (frame[:, :, 0] > frame[:, :, 1]) # r > g
id_gb = (frame[:, :, 1] > frame[:, :, 2]) # g > b
id_rb = (frame[:, :, 0] > frame[:, :, 2]) # r > b
id_rgb_ = np.bitwise_and(id_rg, id_gb)
id_rgb = np.bitwise_and(id_rgb_, id_rb)
#id_max = (frame[:, :, 2] == [255])
#apply the above condition to the mask
thres_mask_red[id_rgb == 0] = [0]
#thres_mask_red[id_max == 0] = [0]


#hsv thresholding
hsv_edit = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.uint8) 

lower_blue = np.array([4,100,220])
upper_blue = np.array([25,260,260])
thres_mask_hsv1 = cv2.inRange(hsv_edit, lower_blue, upper_blue)

lower_blue2 = np.array([50,100,220])
upper_blue2 = np.array([70,260,260])
thres_mask_hsv2 = cv2.inRange(hsv_edit, lower_blue2, upper_blue2)

thres_mask_hsv = cv2.bitwise_or(thres_mask_hsv1, thres_mask_hsv2)

#mask
#thres_mask_hsvnrgb = cv2.bitwise_or(thres_mask_hsv, thres_mask_red)
#bit_mask_three = cv2.bitwise_and(thres_mask_hsvnrgb, thres_mask_y)
thres_mask_ynrgb = cv2.bitwise_or(thres_mask_y, thres_mask_red)
bit_mask_three = cv2.bitwise_and(thres_mask_ynrgb, thres_mask_hsv)
flame_mask = cv2.bitwise_and(frame, frame, mask = bit_mask_three)


#decision making regarding detection
n = cv2.countNonZero(bit_mask_three)
c = 0
pixel_thres = float(n)/float(frame.size)
if pixel_thres > 0.0005: #need to change
   c = 1

#displaying results
plt.subplot(121), plt.imshow(frame)
plt.title('frame'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(flame_mask)
plt.title('res_mix'), plt.xticks([]), plt.yticks([])
plt.figtext(0.7, 0.02, "Pixel Threshold count: "+str(pixel_thres), style='italic', bbox={'facecolor':'blue', 'alpha':0.7, 'pad':10})
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())


if c==1:
    plt.figtext(.02, .02, "FLAME DETECTED\n", style='italic', bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
else:
    plt.figtext(.02, .02, "FLAME NOT DETECTED\n", style='italic', bbox={'facecolor':'green', 'alpha':0.5, 'pad':10})

plt.show()


