"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 2A - Color Image Line Following
"""

########################################################################################
# Imports
########################################################################################
from enum import IntEnum as intem
from os import error
import sys
from threading import local
import cv2 as cv
import numpy as np
sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# >> Constants
# The smallest contour we will recognize as a valid contour
MIN_CONTOUR_AREA = 30

# A crop window for the floor directly in front of the car
CROP_FLOOR = ((360, 0), (rc.camera.get_height(), rc.camera.get_width()))

# Colors, stored as a pair (hsv_min, hsv_max)
BLUE = ((90, 50, 50), (120, 255, 255)) #rgb = max 0,174,239 and low 26,117,155

GREEN = ((105, 224, 140),(104, 255, 170))#rgb = max 0,174,82 and low 50,150,0

RED = ((0, 237, 198),(0, 255, 255))# rgb = max 255,0,0 and low 198,14,14

LIGHT_GREEN = ((127, 51, 50), (85, 255, 255)) #rgb max 60,255,255 and min 40,50,50

#OTHER_COLOR = ((0, 42, 60), (127, 175, 255)) #rgb max 80,255,255
 # The HSV range for the color blue
# TODO (challenge 1): add HSV ranges for other colors

# >> Variables
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour

########################################################################################
# Functions
def update_contour():
    global contour_center
    global contour_area

    image = rc.camera.get_color_image()

    if image is None:
        contour_center = None
        contour_area = 0
    else:
        image = rc_utils.crop(image, CROP_FLOOR[0], CROP_FLOOR[1])

        blue_contours = rc_utils.find_contours(image, BLUE[0], BLUE[1])
        light_green_contours = rc_utils.find_contours(image, LIGHT_GREEN[0], LIGHT_GREEN[1])
        green_contours = rc_utils.find_contours(image, GREEN[0], GREEN[1])
        red_contours = rc_utils.find_contours(image, RED[0], RED[1])
        #other_color_contours = rc_utils.find_contours(image, OTHER_COLOR[0], OTHER_COLOR[1])

        # Prioritize driving towards red over green and blue
        if red_contours:
            contour = rc_utils.get_largest_contour(red_contours, MIN_CONTOUR_AREA)
            if contour is not None:
                contour_center = rc_utils.get_contour_center(contour)
                contour_area = rc_utils.get_contour_area(contour)
                rc_utils.draw_contour(image, contour, color=(0, 255, 0))  # Red contours in blue color
                rc_utils.draw_circle(image, contour_center)
                rc.display.show_color_image(image)
                return  # Exit early to prioritize red

        # If red is not found, prioritize driving towards green over blue
        if green_contours:
            contour = rc_utils.get_largest_contour(green_contours, MIN_CONTOUR_AREA)
            if contour is not None:
                contour_center = rc_utils.get_contour_center(contour)
                contour_area = rc_utils.get_contour_area(contour)
                rc_utils.draw_contour(image, contour, color=(0, 255, 0))  # Green contours in green color
                rc_utils.draw_circle(image, contour_center)
                rc.display.show_color_image(image)
                return  # Exit early to prioritize green
            
            
        if light_green_contours:
            contour = rc_utils.get_largest_contour(light_green_contours, MIN_CONTOUR_AREA)
            if contour is not None:
                contour_center = rc_utils.get_contour_center(contour)
                contour_area = rc_utils.get_contour_area(contour)
                rc_utils.draw_contour(image, contour, color=(144, 238, 144))  # Light green contours
                rc_utils.draw_circle(image, contour_center)
                rc.display.show_color_image(image)
                return  # Exit early to prioritize light green

        # If neither red nor green is found, drive towards blue
        if blue_contours:
            contour = rc_utils.get_largest_contour(blue_contours, MIN_CONTOUR_AREA)
            if contour is not None:
                contour_center = rc_utils.get_contour_center(contour)
                contour_area = rc_utils.get_contour_area(contour)
                rc_utils.draw_contour(image, contour, color=(255, 0, 0))  # Blue contours in red color
                rc_utils.draw_circle(image, contour_center)
        

                # If neither red, green, nor blue is found, drive towards other colors
        #if other_color_contours:
         #   contour = rc_utils.get_largest_contour(other_color_contours, MIN_CONTOUR_AREA)
          #  if contour is not None:
           #     contour_center = rc_utils.get_contour_center(contour)
            #    contour_area = rc_utils.get_contour_area(contour)
             #   rc_utils.draw_contour(image, contour, color=(255, 255, 0))  # Other color in yellow color
              #  rc_utils.draw_circle(image, contour_center)
               # rc.display.show_color_image(image)
                #return  # Exit early to prioritize other colors


        else:
            contour_center = None
            contour_area = 0

        rc.display.show_color_image(image)






def start():
    """
    This function is run once every time the start button is pressed
    """
    
    global Anglecaculator
    global speed
    global angle

    # Initialize variables
    speed = 0
    angle = 0

    # Set initial driving speed and angle
    rc.drive.set_speed_angle(speed, angle)

    # Set update_slow to refresh every half second
    rc.set_update_slow_time(0.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)

    # Print start message
    print(
        ">> Lab 2A - Color Image Line Following\n"
        "\n"
        "Controls:\n"
        "    Right trigger = accelerate forward\n"
        "    Left trigger = accelerate backward\n"
        "    A button = print current speed and angle\n"
        "    B button = print contour center and area"
    )


def update():
    global speed
    global angle
    global Angle_error

    # Search for contours in the current color image
    update_contour()

    Angle_error = 0

    # Choose an angle based on contour_center
    # If we could not find a contour, keep the previous angle
    if contour_center is not None:
        Angle_error = (contour_center[1] - 320) / 320  # Current implementation: bang-bang control (very choppy)
        # TODO (warmup): Implement a smoother way to follow the line
        # if contour_center[1] < rc.camera.get_width() / 8:
        #    angle = Anglecaculator
        # else:
        #    angle = -Anglecaculator

    # Use the triggers to control the car's speed
    forwardSpeed = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    backSpeed = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
    speed = forwardSpeed - backSpeed

    

    # If contour is found, use the calculated angle; otherwise, use the last known angle
    if contour_center is not None:
        angle = 1 * Angle_error


    if abs(angle) > 0.49 :
        speed = speed/1.5
    rc.drive.set_speed_angle(speed, angle)

    
    # Print the current speed and angle when the A button is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # Print the center and area of the largest contour when B is held down
    if rc.controller.is_down(rc.controller.Button.B):
        if contour_center is None:
            print("No contour found")
        else:
            print("Center:", contour_center, "Area:", contour_area, "camera width", rc.camera.get_width())


def update_slow():
    """
    After start() is run, this function is run at a constant rate that is slower
    than update().  By default, update_slow() is run once per second
    """
    # Print a line of ascii text denoting the contour area and x-position
    #if rc.camera.get_color_image() is None:
    #    # If no image is found, print all X's and don't display an image
    #    print("X" * 10 + " (No image) " + "X" * 10)
    #else:
    #    # If an image is found but no contour is found, print all dashes
    #    if contour_center is None:
    #        print("-" * 32 + " : area = " + str(contour_area))

        # Otherwise, print a line of dashes with a | indicating the contour x-position
    #    else:
    #        s = ["-"] * 32
    #        s[int(contour_center[1] / 20)] = "|"
    #        print("".join(s) + " : area = " + str(contour_area))


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
