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
import math

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Add any global variables here

depthPoints = (
    1/3, 2/3
)

changePoints = (100, 200)
isBackingUp = False

wallAngle = 0

stopDistance = 15
slowDistance = 80

cropCoord = (
    (0, rc.camera.get_width() * 1 // 5),
    (rc.camera.get_height() // 3, rc.camera.get_width() * 4 // 5 + 10)
)

accurateDepth = [0, 0, 0, 0, 0]

########################################################################################
# Functions
########################################################################################

def calculerVitesse(distance):
    global stopDistance
    global slowDistance

    if distance < stopDistance:
        return 0.5

    correction = 2 if distance < stopDistance else -2

    speed = distance + correction

    speed -= stopDistance
    speed /= slowDistance

    speed *= abs(speed) * 0.8
    return speed


def start():
    """
    This function is run once every time the start button is pressed
    """

    global isBackingUp

    # Have the car begin at a stop
    rc.drive.stop()

    isBackingUp = 0

    # Print start message
    print(">> Lab 3C - Depth Camera Wall Parking")


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """

    global depthPoints
    global cropCoord
    global accurateDepth
    global isBackingUp


    angle = 0

    depth_image = rc.camera.get_depth_image()


    depthPixels = []

    for i in depthPoints:
        #depthPixels.append(depth_image["""rc.camera.get_height() // 2"""][rc.camera.get_width() * i // 1])
        depthPixels.append((depth_image[5][math.floor(rc.camera.get_width() * i)] - 0.1) % 1000)

    depthDiff = depthPixels[0] - depthPixels[1]

    if depthDiff > 1:
        angle = 0.8
    elif depthDiff < 1:
        angle = -0.8


    depth_image = rc_utils.crop(depth_image, cropCoord[0], cropCoord[1])
    minPixel = rc_utils.get_closest_pixel(depth_image)
    minDistance = depth_image[minPixel[0]][minPixel[1]]


    speed = calculerVitesse((minDistance + sum(accurateDepth) / 8) / 2)

    accurateDepth.append(minDistance)

    if len(accurateDepth) > 8:
        accurateDepth.pop(0)

    speed = 0.8 if speed > 0.8 else -0.8 if speed < -0.8 else 0 if abs(speed) < 0.02 else speed
    angle = -angle if speed < 0 else angle

    print("~~~")
    print(sum(accurateDepth) / 8)
    print(depthDiff)
    #rc.drive.set_speed_angle(rc.controller.get_trigger(rc.controller.Trigger.RIGHT) - rc.controller.get_trigger(rc.controller.Trigger.LEFT), rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0])
    rc.drive.set_speed_angle(speed, angle)
    


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
