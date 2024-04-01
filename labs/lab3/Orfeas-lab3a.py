"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 3A - Depth Camera Safety Stop
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

stopDistance = 40
slowingDistance = 80

#hueCutoff = 33

cropCoord = (
    (0, rc.camera.get_width() * 2 // 5 - 10),
    (rc.camera.get_height() // 3, rc.camera.get_width() * 3 // 5 + 10)
)

redValues = ((170, 50, 50), (10, 255, 255))

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
    print(
        ">> Lab 3A - Depth Camera Safety Stop\n"
        "\n"
        "Controls:\n"
        "    Right trigger = accelerate forward\n"
        "    Right bumper = override safety stop\n"
        "    Left trigger = accelerate backward\n"
        "    Left joystick = turn front wheels\n"
        "    A button = print current speed and angle\n"
        "    B button = print the distance at the center of the depth image"
    )


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """

    global stopDistance
    global slowingDistance

    #global hueCutoff

    global cropCoord
    global redValues


    # Use the triggers to control the car's speed
    speed = rc.controller.get_trigger(rc.controller.Trigger.RIGHT) - rc.controller.get_trigger(rc.controller.Trigger.LEFT)

    # Calculate the distance of the object directly in front of the car
    depth_image = rc.camera.get_depth_image()
    color_image = rc.camera.get_color_image()

    colourContour = rc_utils.find_contours(color_image, redValues[0], redValues[1])
    colourContour = rc_utils.get_largest_contour(colourContour, 20)


    minDistance = 999

    if colourContour is not None:
        contourCenter = rc_utils.get_contour_center(colourContour)
        minDistance = depth_image[contourCenter[0]][contourCenter[1]]
        print("help")

    else:
        depth_image = rc_utils.crop(depth_image, cropCoord[0], cropCoord[1])
        minPixel = rc_utils.get_closest_pixel(depth_image)
        minDistance = depth_image[minPixel[0]][minPixel[1]]
        print("me")

    minDistance = 999 if minDistance <= 0.05 else minDistance


    if minDistance < stopDistance + slowingDistance:
        print("hey why")
        speed = -0.1


    if speed < -0.8:
        speed = -0.8
    elif speed > 1:
        speed = 1


    # Use the left joystick to control the angle of the front wheels
    angle = rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0]

    # Print the current speed and angle when the A button is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # Print the depth image center distance when the B button is held down
    if rc.controller.is_down(rc.controller.Button.B):
        print("Center distance:", minDistance)

    # Display the current depth image
    rc.display.show_depth_image(depth_image)

    print(minDistance)
    print(speed)

    rc.drive.set_speed_angle(speed, angle)


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
