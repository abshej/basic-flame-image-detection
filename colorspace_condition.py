#author: Avadhoot S
"""
Basic conditions in many research papers for flame detection is 
R > G > B in RGB color model
and 
Y > Cr > Cb in YUV color model
this program checks both(AND logic) of conditions in an image
"""
import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys

#image acquisition
img = cv2.cvtColor(cv2.imread(str(sys.argv[1]), -1), cv2.COLOR_BGR2RGB) #in RGB
image = img.copy() #create copy of image

#r > g > b
id_rg = (image[:, :, 0] > image[:, :, 1]) # r > g
id_gb = (image[:, :, 1] > image[:, :, 2]) # g > b
id_rb = (image[:, :, 0] > image[:, :, 2]) # r > b
id_rgb_ = np.bitwise_and(id_rg, id_gb)
id_rgb = np.bitwise_and(id_rgb_, id_rb)

#convert to ycrcb format
image_ = cv2.cvtColor(img, cv2.COLOR_RGB2YCR_CB)

#y > cr > cb
id_ycr = (image_[:, :, 0] > image_[:, :, 1]) # y > cr
id_crcb = (image_[:, :, 1] > image_[:, :, 2]) # cr > cb
id_ycb = (image_[:, :, 0] > image_[:, :, 2]) # y > cb
id_ycrcb_ = np.bitwise_and(id_ycr, id_crcb) 
id_ycrcb = np.bitwise_and(id_ycrcb_, id_ycb)

#r>g>b AND y>cr>cb
id_both = np.bitwise_and(id_rgb, id_ycrcb) #combining using AND logic

#blacking out rest of the pixels
image[id_both == 0] = [0, 0, 0]

#display results
plt.subplot(121), plt.imshow(img)
plt.title('Original')
plt.subplot(122), plt.imshow(image)
plt.title('Result')
plt.show()
