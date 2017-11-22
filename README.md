

*basic-flame-detection*

Detect flames in video or static image frames using image processing

**using_colorspaces.py uses thresholding on different colorspaces to detect possible flame pixels
**colorspace_condition.py uses basic RGB and YUV color model condition for each pixel in an image to filter possible flame pixels
**with_PiCamera.py takes video feed from a Raspberry Pi's Pi Camera module and detects flames in image frames using colorspace thresholding algorithm from using_colorspaces.py

*Image Frame should be given as the first argument after script names ( expect for with_PiCamera.py)

[Does give false positives]

---Tweaking the threshold values or adding more ranges and bitwise logic to enable more accurate detection in varying types of images is encouraged

---colorspace_condition.py is ideally to be included as a condition in using_colorspaces.py

---The framerate and video resolution in with_PiCamera.py can be changed as per user's choice and Pi's performance
