# basic-flame-detection
Detect flames in image frames 

Image Frame should be given as the first argument after script names

Doesn't work with stock images of flames with dark or black backgrounds
It will work with those images if you tweak the threshold values or add a bias for YCbCr mask, that is, use that with a bitwise_or along with the HSV 'or' RGB mask.
