# Lab 4
### Group 21 [zz2517, ayz2103, jx2324]
### Youtube link: 
- Basic credit: https://www.youtube.com/watch?v=wGJ8tMJu90Q&feature=youtu.be
- Extra credit: https://www.youtube.com/watch?v=b16zSi3zgSU&feature=youtu.be

You can find our main and helper functions in `lane_follower.py`.

You can find our main and helper functions of the extra credit part in `lane_follower_extra.py`

We made the following assumptions about our robot/environment: 
- The robot car starts with the yellow line already in the center of the car body.
- The sizes of pictures taken are set to be 320 * 240 pixcels, the sizes of homographies after transformation are also set to be 320 * 240 pixels
- We are using the dots which forms a rectangule of 32cm * 24cm in reality to calculate our homography transformation matrix, so we know: 1 pixel in homography = 0.1cm in reality.
- We are using our own functions `rotate_right_small()` and `rotate_left_small()` to adjust the direction of our robot when there is an angle offset. These functions rotate the robot using time. They rotates the robot for 0.1s with a small speed. In this way, we can achieve a very tiny rotation which makes our adjustments very precise. In comparison, if we use encoders to rotate the robot (using both wheels), the smallest degree we can turn is theoretically ~11 degree (1 encoder).

## Values calculated from ta_supplied_image_set:
calculated_angle_offset = 2.8274333477020264 degrees

calculated_distance_offset = 14.752297917018172 cm

homography_transform_matrix = 

[[  2.13566102e+01   2.64821966e+01  -3.54519729e+03]

 [ -2.32304805e+00   1.02214114e+02  -7.49647605e+03]
 
 [ -8.79290451e-03   1.67931598e-01   1.00000000e+00]]
 
distance_to_camera_from_homography = 17.765899863094143 cm

## Values calculated from student_captured_image_set:
calculated_angle_offset = 0.10471975803375244 degrees

calculated_distance_offset = 0.77673682515970777 cm

homography_transform_matrix = 

[[  2.75129002e+00   1.75082092e+00  -3.04392723e+02]

 [ -5.24680465e-01   1.12431528e+01  -5.90265523e+02]
 
 [ -3.01666667e-03   1.59796254e-02   1.00000000e+00]]
 
distance_to_camera_from_homography =  22.505883596471483 cm

## Questions:
#### 1. Describe the overall architecture of your implementation.
The robot repeatedly takes images to help it make decision for the following movements. It processes the images and moves in the routines below:
1. Before using the homography transformation matrix to find the region of interest in the image, we first draw magenta line in the center of the image. 
2. Use HSV of yellow and HSV of orange to threshold and binarize the image separately. We also implement **dilation** and **erosion** in this step to find a more accurate region. This step gives us two masks for yellow and orange each.
3. For the mask of yellow, we implement canny algorithm to find the edges, then implement hough line algorithm to find the parameters of lines of edges. This step gives us a list of rhos and thetas.
4. For those line parameters returned, we only take the top two lines, which are lines getting most votes. We draw those lines on the homography, so that we can visualize the offset between the yellow line and the magenta line.
5. We use the thetas, rhos and the region of orange (orange mask) to help the robot maintain the following status: the direction of the robot is parallel to the yellow line; the yellow line is in the center of the robot in most time; the robot will make a U-turn when it sees an orange line. The detailed logic to control the flow is given in Question 4.

#### 2. What method did your group use to calculate the distance from the center line?
This implementation can be found in `compute_distance()` from `lane_follower.py`

The distance from the center line is defined as the shortest distance from the camera to the yellow line. Since we know the distance from the camera to the bottom pixel of the homogrophy picture, and we know the correspondence between pixel and cm (1 pixel in homography = 0.1cm in reality), we can easily get the position of the camera in the homography: (x, y), where x = 160, y = 240 + distance_to_camera_from_homography/0.1. Since we also know the parameters of the yellow line returned by `canny_and_hough()` function in the form (rho, theta), we can calculate the distance by: d = ((x * cos(theta) + y * sin(theta)) - rho) * 0.1 cm. In this way, d is negative if the robot is to the left of the yellow line and positive if to the right of the yellow line.

#### 3. What method did your group use to calculate the angle offset from the center line?
The  angle offset from the yellow line to the magenta is defined as the difference in degree of the slopes between yellow lines and magenta. We first modify the theta to find the slope of lines in degrees. The slope of magenta (theta_magenta) is always 90 degrees in our homography frame, which is always parallel to the y-axis. For the theta values returned from hough line algorithm, we add 90 degrees to those thetas smaller than 90 and subtract 90 degrees from those thetas greater than 90. By doing this, we get the slope (in degrees) of yellow line (theta_yellow). In this way, angle_offset = theta_yellow - theta_magenta. If angle_offset is negative, the robot needs to turn left while it needs to turn right if angle_offset is positive.

#### 4. Describe your control flow algorithm based on distance, angle, and whatever other metrics you used.
Our robot starts with the yellow line as center line. In every iteration, it takes a picture and then uses the methods mentioned in Question 2 and 3 to calculate the angle and distance offsets from the homography. If the absolute value of angle offset is bigger than 1 degree, we adjust the direction of our robot by: turning a tiny amount of degree (~1) right if angle offset is positive, turning a tiny amount of degree (~1) left if angle offset is negative. If the angle offset is between -1 and 1 (including -1 and 1), then we assume the robot is going parallel with the yellow line, then we use the distance offset to judge whether the robot is too far away from the yellow line. Turn left if the distance offset is < -5 and turn right if the distance offset is > 5.

It is worth noting that because we have a tolerance of 1 degree for the angle offset (if the offset is +1 or -1 we assume it is still going parallel with the yellow line), it is possible that the robot keeps going the direction with 1 degree offset, so that it misses the yellow line while moving, given the distance offset tolerance we have. To handle this, when the yellow line cannot be seen by the robot (still very unlikely even possible), we also need to rotate the robot based on the its direction in the previous loop. `needTurnLeft = True` means the robot was previously to the right side of the yellow line, so when it cannot see the yellow line, it turns left, and the same logic for `needTurnRight = True`.

We use the orange mask in every iteration to find the number of pixels of orange in the homography. If we find an area of more than 2000 orange pixels then we consider that the robot has seen the orange line. After this, we move forward the robot for the amount of distance_to_camera_from_homography and then rotate back. Because the rotation functions from gopigo is quite imprecise and the robot might have a large angle offset before U-turn as a result of the big moving-forward it does after seeing the orange line, we only rotate the robot for 15 encoders and then iteratively use the `rotate_left_small()` function until it rotates within the acceptable angle offset range. Then it starts moving forward and repeats all the steps.

#### 5. What is the purpose of the distance offset from the camera to the homography transform?
By knowing the distance offset from the camera to the homography transform, the robot will know how far away its camera is looking at. This value is helpful in two scenarios:

- First, when the robot sees the orange line, it can know exactly how far it can move forward before hitting the orange line, and then it makes a U-turn accordingly. 
- Second, this distance is used in calculating the distance offset of the robot from the center line, as described in Question 2.

The method we calculate this distance is first defining bottom_middle_pixel = [160, 240, 1], which is the coordinate of the bottom middle pixel in the original image before homography. Then we find the corresponding coordinate of this pixel in the homography by computing the dot product of homography matrix and bottom_middle_pixel. After normalizing z value, we can find the corresponding y in homography. Afterwards, we compute the difference between the corresponding y and 240, this will give us the distance in pixels from camera to the bottom of homography. After multiplying this distance with 0.1 cm, we finally find this distance in centimeters, which is distance_to_camera_from_homography. This is implemented in function `find_cameratohomo()` in `lane_follower.py`
