"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 3B - Depth Camera Cone Parking
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

correction_timer = 0
ORANGE = ((10, 100, 100), (20, 255, 255))

########################################################################################
# Functions
########################################################################################


def start():
    """
    This function is run once every time the start button is pressed
    """
    # Have the car begin at a stop
    rc.drive.stop()

    # Print start message
    print(">> Lab 3B - Depth Camera Cone Parking")


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    
    global correction_timer
    global ORANGE

    speed = 0.6
    angle = 0

    image = rc.camera.get_color_image()

    contour = rc_utils.find_contours(image, ORANGE[0], ORANGE[1])
    contour = rc_utils.get_largest_contour(contour, 20)
    
    contour_center = rc_utils.get_contour_center(contour)


    #now we shall go out of our way to find the angles
    angle = 2 * contour_center[1] - rc.camera.get_width()
    angle = angle / rc.camera.get_width()


    depth = rc.camera.get_depth_image()

    contour_distance = depth[contour_center[0]][contour_center[1]]


    if speed < -0.8:
            speed = -0.8
    elif speed > 0.8:
        speed = 0.8
    elif abs(speed) < 0.05:
        speed = 0

    if speed != 0:
        angle *= speed / abs(speed)

    speed /= 1.5


    if contour_distance < 30:
        speed = -0.2
    if contour_distance < 31 and contour_distance > 29:
        speed = 0


    if speed == 0 and abs(contour_center[1] - rc.camera.get_width() / 2) > 200:
        correction_timer = 1    

    if correction_timer > 0:
        speed = -0.8
        angle *= -1
        correction_timer -= rc.get_delta_time()

    rc.drive.set_speed_angle(speed, angle)
    print(contour_distance)
    print("Speed:", speed, "Angle:", angle)


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
