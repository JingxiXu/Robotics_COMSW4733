from gopigo import *
import random
import time
import os

GLOBAL_SPEED = 46

class Dance():
    grooves = [stop, fwd, bwd, left, right, left_rot, right_rot]
    speed = [GLOBAL_SPEED, GLOBAL_SPEED, GLOBAL_SPEED, 100, 100, 80, 80]

    def __init__(self, command, speed=None,):
        self.move = Dance.grooves[command]
        if speed == None:
            set_speed(Dance.speed[command])

    def __enter__(self):
        self.move()

    def __exit__(self, *args):
        set_speed(GLOBAL_SPEED)
        stop()

def timeMonitor(moveTime, startTime):
    if os.times()[4] - startTime + moveTime < 20:
        time.sleep(moveTime)
    else:
        dur = 20 - os.times()[4] + startTime
        time.sleep(dur if dur > 0 else 0)

def main():
    servo(105)

    enable_com_timeout(20000)
    startTime = os.times()[4]
    pre_command = 0
    command = 0
    while os.times()[4] - startTime < 20:
        while command == pre_command:
            command = random.randint(1,6)

        with Dance(command):
            moveTime = random.randint(1,3)
            timeMonitor(moveTime, startTime)
            
        pre_command = command

    stop()
    print(os.times()[4]-startTime)

if __name__ == "__main__":
    main()
