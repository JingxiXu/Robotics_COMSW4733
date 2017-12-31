import time
from gopigo import *

DURATION = 0.02
CORRECTION = 1.29

def main():
    distances = []
    for position in range(0, 180):
        servo(position)
        # time.sleep(1)
        corrected = round(us_dist(15)/CORRECTION)
        #distances.append(round(corrected/20))
        distances.append(corrected)
    # count all the values lower than 20.
    # that is the number of positions where the robot can detect the object
    angle = sum(i < 20 for i in distances)
    # print(distances)
    # print("num of elements: {}".format(len(distances)))
    print("Beam width angle is: {} degrees".format(angle))

def hand_test():
    distance = us_dist(15)/CORRECTION
    while distance > 5:
        print(distance)
        distance = us_dist(15)/CORRECTION

if __name__ == "__main__":
    main()
