

*basic-flame-detection*

Detect flames in image frames using image processing

**using_colorspaces.py uses thresholding on different colorspaces to detect possible flame pixels
**colorspace_condition.py uses basic RGB and YUV color model condition for each pixel in an image to filter possible flame pixels

*Image Frame should be given as the first argument after script names

[Does give false positives]

Tweaking the threshold values or adding more ranges and bitwise logic to enable more accurate detection in varying types of images is encouraged

colorspace_condition.py is ideally to be included as a condition in using_colorspaces.py
