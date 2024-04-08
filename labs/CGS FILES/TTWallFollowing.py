"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020
"""

########################################################################################
# Imports
########################################################################################

import sys
import cv2 as cv
import numpy as np

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils

rc = 0

########################################################################################
# Functions
########################################################################################

def setUp(raceCar):
    global rc
    rc = raceCar
    print("Wall Following set up successfully!")


def find_first_opening(scan):
    start_point = scan[180]
    last = start_point
    current_index = 180
    while current_index > 0:
        if abs(last - scan[current_index]) > 10:
            return current_index + 10
        last = scan[current_index]
        current_index =- 1
    return 0


def start():
    """
    This function is run once every time the start button is pressed
    """
    # Have the car begin at a stop
    rc.drive.stop()


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    # TODO: Follow the wall to the right of the car without hitting anything.
    scan = rc.lidar.get_samples()
    
    closest_point_index = rc_utils.get_lidar_closest_point(scan, (0, 180))
    if closest_point_index[1] == 0: closest_point_index[1] = 99999
    closest_point_left = rc_utils.get_lidar_closest_point(scan, (180, 360))
    
    #print(closest_point_left[1])

    if closest_point_index[0] > 93: angle = 1
    elif closest_point_index[0] < 87: angle = -1
    #elif closest_point_left[0] > 350: angle = -1
    else: angle = (find_first_opening(scan) / 180)

    if closest_point_left[1] < 10:
        angle += 0.1
    
    if scan[0] == 0:
        speed = 1
    else:      
        speed = scan[0]/50
    
    rc.drive.set_speed_angle(min(max(-0.5,speed), 0.5), min(max(-1,angle), 1))


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc = racecar_core.create_racecar()
    rc.set_start_update(start, update, None)
    rc.go()
