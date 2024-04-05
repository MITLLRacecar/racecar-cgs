"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Phase 1 Challenge - Cone Slaloming
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

RED = ((170, 50, 50), (10, 255, 255))
BLUE = ((100, 150, 50), (110, 255, 255))

min_contour_area = 30

cropping_min = (320, 0)
cropping_max = (rc.camera.get_height(), rc.camera.get_width())

contour_area = 0
contour_center = (None, None)

prev_cone_color = ""


########################################################################################
# Functions
########################################################################################


def update_ConeSlaloming():
    
    # Bang-Bang Control the Angle
    # Proportional Control the Speed

    global prev_cone_color
    global contour_area
    global contour_center

    update_contour()

    if contour_center == None:
        rc.drive.set_speed_angle(1, 0)
        return

    
    depth_image = rc.camera.get_depth_image()
    depth_image = rc_utils.crop(depth_image, cropping_min, cropping_max)


    angle = 0

    # TODO RED_param and BLUE_param and their sum

    if angle < -1:
        angle = -1
    elif angle > 1:
        angle = 1
    elif angle == 0:
        if prev_cone_color == "Red":
            angle = -1
        else:
            angle = 1


    cone_distance = 0

    if prev_cone_color == "Red" and contour_center[0] is not None:
        cone_distance = depth_image[contour_center[0][0]][contour_center[0][1]]
    elif prev_cone_color == "Blue" and contour_center[1] is not None:
        cone_distance = depth_image[contour_center[1][0]][contour_center[1][1]]


    speed = 1

    # TODO Proportional Control the speed based on cone_distance


    #rc.drive.set_speed_angle(speed, angle)
    rc.drive.set_speed_angle(rc.controller.get_trigger(rc.controller.Trigger.RIGHT) - rc.controller.get_trigger(rc.controller.Trigger.LEFT), rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0])
    #print(rc.camera.get_width())


def update_contour():
    
    # Sets contour_center to (RED_contour_center, BLUE_contour_Center).
    # Sets prev_cone_color to the color of the closest cone, if one is found.
    # Sets contour_area to the area of the closest cone and if none is found, sets it to 0.

    global prev_cone_color
    global contour_center
    global contour_area
    global min_contour_area
    global cropping_min
    global cropping_max

    image = rc.camera.get_color_image()

    if image is None:
        contour_center = None
        contour_area = 0

    else:
        image = rc_utils.crop(image, cropping_min, cropping_max)

        BLUE_contour_list = rc_utils.find_contours(image, BLUE[0], BLUE[1])
        RED_contour_list = rc_utils.find_contours(image, RED[0], RED[1])

        BLUE_contour = None
        RED_contour = None

        if BLUE_contour_list:
            BLUE_contour = rc_utils.get_largest_contour(BLUE_contour_list, min_contour_area)

        if RED_contour_list:
            RED_contour = rc_utils.get_largest_contour(RED_contour_list, min_contour_area)


        if RED_contour is not None and BLUE_contour is not None:

            RED_contour_center = rc_utils.get_contour_center(RED_contour)
            BLUE_contour_center = rc_utils.get_contour_center(BLUE_contour)

            contour_center = (RED_contour_center, BLUE_contour_center)


            BLUE_contour_area = rc_utils.get_contour_area(BLUE_contour)
            RED_contour_area = rc_utils.get_contour_area(RED_contour)

            if RED_contour_area >= BLUE_contour_area:
                contour_area = RED_contour_area
                prev_cone_color = "Red"
            else:
                contour_area = BLUE_contour_area
                prev_cone_color = "Blue"


        elif RED_contour is not None:
            contour_center = (rc_utils.get_contour_center(RED_contour), None)
            contour_area = rc_utils.get_contour_area(RED_contour)
            prev_cone_color = "Red"

        elif BLUE_contour is not None:
            contour_center = (None, rc_utils.get_contour_center(BLUE_contour))
            contour_area = rc_utils.get_contour_area(BLUE_contour)
            prev_cone_color = "Blue"

        else:
            contour_center = (None, None)
            contour_area = 0
            



def start():
    rc.drive.stop()

    global cone_color
    global contour_area
    global contour_center

    cone_color = ""
    contour_area = 0
    contour_center = (None, None)

    print(">> Time Trial: Cone Slaloming")


def update():
    update_ConeSlaloming()




########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
