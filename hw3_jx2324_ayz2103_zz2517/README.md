This is a Lab 3 submission for group 21

Team Members
============
Zhang Zhang (zz2517), Jingxi Xu (jx2324), Aryeh Yonatan Zapinsky (ayz2103)

Robot Name: Mark 38

Youtube link for bug2 demo: https://www.youtube.com/watch?v=tdP_BHdL5Do

Implementation
==============
The robot first takes an image to allow users to draw a rectangular region of interest. The RGB values stored in the region of interest are then transfromed into HSV space to get rid of the influence of illumination change. Then the maximum and minimum values of Hue, Saturation, Value respectively in the region are used as the threshold to detect the color in following steps. We build the binary image by applying the threshold over each image. To have a better performance in detecting the color, we made the following improvements:
* implemented a 5 by 5 box filter over each image taken
* implemented dilation with 10 iterations to connect small blobs as much as possible
* relaxed the thresholds of Saturation and Value mannually

What's more, the centroid and diameter of the biggest blob found in the first image will be the reference for the following images to move.

While the algorithm is running, the robot will consecutively take images and compute the centroid position and diameter of the biggest blob of each image. To help the robot move stable, before every movement, we first take 6 images and then use the median of these centroid positions and diameters to evaluate the position of target color in robot's current vision. Then the robot will move accordingly to change the size and position of the biggest blob to be the same as that of the initial photo. 

Assumptions
===========
* The robot will not response to the change in blob size within 12 pixels. 

* The robot will not response to the horizonal changes in blob position which are within a quarter of the initial blob size.

* The robot will not response to any vertical change in blob position.
