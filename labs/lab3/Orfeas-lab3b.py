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

stopDistance = 30
slowDistance = 20

orangeValues = ((10, 100, 100), (20, 255, 255))
minContourArea = 20

########################################################################################
# Functions
########################################################################################

def calculerVitesse(distance):
    global stopDistance
    global slowDistance

    correction = -2 if distance < stopDistance else 2

    speed = distance

    speed -= stopDistance + correction
    speed /= slowDistance

    speed *= abs(speed)
    return speed

def calculerAngle(position):
    halfWidth = rc.camera.get_width() / 2
    return 0.9 * (position - halfWidth) / halfWidth

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
    angle = 0
    speed = 1

    colorImage = rc.camera.get_color_image()
    
    if colorImage is None:
        return
    
    allContours = rc_utils.find_contours(colorImage, orangeValues[0], orangeValues[1])
    contour = rc_utils.get_largest_contour(allContours, minContourArea)

    if contour is None:
        rc.drive.set_speed_angle(0.4, 0.8)
        return
    
    contourCenter = rc_utils.get_contour_center(contour)


    depthImage = rc.camera.get_depth_image()

    if depthImage is None:
        rc.drive.set_speed_angle(0.4, 0.8)
        return
    
    centerDistance = depthImage[contourCenter[0]][contourCenter[1]]


    speed = calculerVitesse(centerDistance)

    angle = calculerAngle(contourCenter[1])


    speed = -0.8 if speed < -0.8 else 0.8 if speed > 0.8 else 0 if abs(speed) < 0.03 else speed

    #if speed < 0:
    #    angle *= -1

    print("~~~")
    print("Distance ", centerDistance)
    print("Speed ", speed)
    print("Angle", angle)
    rc.drive.set_speed_angle(speed, angle)


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
