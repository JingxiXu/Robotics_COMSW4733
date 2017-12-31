from gopigo import *
import math
import time


STOP_DISTANCE = 20
START_DISTANCE = 60
ERROR = 28

DISTANCE_CORRECTION_FACTOR = 1.29

SCAN_SPEED = 46
SCAN_DURATION = 20

def measure_dist():
    return round(us_dist(15)/DISTANCE_CORRECTION_FACTOR)

def normalize_servo():
    servo(104)

def scan_sequence():
    measurements = []
    measurements.append(measure_dist())

    while measurements[-1] > START_DISTANCE + ERROR:
        right_rot()
        time.sleep(0.25)
        stop()
        time.sleep(0.25)
        measurements.append(round(measure_dist()))

def advance():
    ADVANCE_DISTANCE = 1
    fwd(ADVANCE_DISTANCE)

def retreat():
    RETREAT_DISTANCE = 1
    bwd(RETREAT_DISTANCE)

def main():
    normalize_servo()
    set_speed(SCAN_SPEED)

    while measure_dist() > STOP_DISTANCE:
        scan_sequence()
        advance()

    stop()

    # while measure_dist() < STOP_DISTANCE:
    #     retreat()
    #
    # stop()

    print measure_dist()

if __name__ == "__main__":
    main()
