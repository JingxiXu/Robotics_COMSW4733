from gopigo import *
import time

# set the sensor facing stright forward
servo(104)

# wait for the sensor to rotate to the direction perpendicular to the robot
time.sleep(3)

# print out the distance
print(us_dist(15))
