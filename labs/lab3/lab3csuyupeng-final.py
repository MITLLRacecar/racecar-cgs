"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 3C - Depth Camera Wall Parking
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

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Add any global variables here

correction = 1

########################################################################################
# Functions
########################################################################################


def start():
    """
    This function is run once every time the start button is pressed
    """
    global correction
    
    correction = 0.5
    
    # Have the car begin at a stop
    rc.drive.stop()

    # Print start message
    print(">> Lab 3C - Depth Camera Wall Parking")
    


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """

    global correction

    if correction > 0:
        correction -= rc.get_delta_time()
        rc.drive.set_speed_angle(-1, 0)
        return

    angle = 0
    speed = 0.5

    depth = rc.camera.get_depth_image()

    point1 = depth[rc.camera.get_height() // 2][0]
    point2 = depth[rc.camera.get_height() // 2][rc.camera.get_width() - 1]
    point0 = (point1 + point2) / 2

    if point0 == 0:
        point0 = 999
    
    if point1 == 0:
        point1 = 999

    if point2 == 0:
        point2 = 999

    if point1 - point2 > 0.5:
        angle = 0.6
    elif point2 - point1 > 0.5:
        angle = -0.6

    if point1 == 999 and point2 == 999:
        angle = 0.6
        speed = 0.8

    if point0 < 24:
        speed = -0.5
    
    if point0 < 21 and point0 > 19:
        speed = 0

    if speed < -1:
        speed = -1
    elif speed > 1:
        speed = 1
    elif speed < 0.1 and speed > -0.1:
        speed = -0.02

    if speed < 0:
        angle = -angle

    #else:
    rc.drive.set_speed_angle(speed, angle)

    print("~~~")
    print(point1)
    print(point2)
    print(abs(point1 - point2))


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
