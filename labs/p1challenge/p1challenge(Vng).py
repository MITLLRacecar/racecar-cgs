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
from enum import Enum

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

RED = ((160, 0, 0), (179, 255, 255))
BLUE = ((90, 120, 120), (120, 255, 255))

########################################################################################
# Utility Functions
########################################################################################
class State(Enum):
    """
    Enum class representing different states of the car.
    """
    search = 0
    red = 1
    blue = 2
    linear = 3

class Color(Enum):
    """
    Enum class representing different colors detected by the camera.
    """
    RED = 0
    BLUE = 1
    BOTH = 2
    
cur_state = State.search
color_priority = Color.RED

speed = 0.0
angle = 0.0
last_distance = 0
counter = 0

def update_contours(image):
    """
    Finds contoours for the blue and red cone using color image
    """

    MIN_CONTOUR_AREA = 800

    # If no image is fetched
    if image is None:
        contour_center = None
        contour_area = 0

    # If an image is fetched successfully
    else:
        # Find all of the red contours
        contours = rc_utils.find_contours(image, RED[0], RED[1])

        # Find all of the blue contours
        contours_BLUE = rc_utils.find_contours(image, BLUE[0], BLUE[1])

        # Select the largest contour from red and blue contours
        contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA)
        contour_BLUE = rc_utils.get_largest_contour(contours_BLUE, MIN_CONTOUR_AREA)
        #print(rc_utils.get_contour_area(contour_BLUE))

        # Draw a dot at the center of this contour in red
        if contour is not None and contour_BLUE is not None: # checks if both are valid

            contour_area = rc_utils.get_contour_area(contour)
            contour_area_BLUE = rc_utils.get_contour_area(contour_BLUE)
            # if the contour areas are similar enough, indicate that it is a checkpoint
            if abs(contour_area - contour_area_BLUE) < 700:
                return None, Color.BOTH

            # If red contour is bigger than the blue one
            elif contour_area > contour_area_BLUE:
                return contour, Color.RED

            # If blue contour is equal to or bigger than the red one
            else:
                return contour_BLUE, Color.BLUE

        elif contour is None and contour_BLUE is not None:
            return contour_BLUE, Color.BLUE

        elif contour_BLUE is None and contour is not None: 
            return contour, Color.RED

        else:
            # No contours found
            return None, None

########################################################################################
# Environment Interaction Functions
########################################################################################

def start():
    """
    This function is run once every time the start button is pressed
    """

    # Globals
    global cur_state
    global speed,angle,last_dist,counter

    speed = 0.0
    angle = 0.0
    last_dist = 0
    counter = 0
    cur_state = State.search
    # Have the car begin at a stop
    rc.drive.stop()
    


    # Print start message
    print(">> Phase 1 Challenge: Cone Slaloming")

def update_slow():
    """
    This function is run every frame when the update is in slow mode.
    """
    pass

def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed

    Working with depth camera, fetching contour stuff from update_contours
    """

    # Globals
    global cur_state
    global speed
    global angle
    global color_priority
    global last_dist
    global counter

    # Reset speed and angle variables
    speed = 0.0
    angle = 0.0
    distance = 5000
    dist_param = 200

    # TODO: Slalom between red and blue cones.  The car should pass to the right of
    # each red cone and the left of each blue cone.

   # Fetch color and depth images
    ImageDepth = rc.camera.get_depth_image()
    image = rc.camera.get_color_image()

    # Crop the images
    camera_height = (rc.camera.get_height() // 10) * 10
    camera_width = (rc.camera.get_width() // 10) * 10

    tli = (0, rc.camera.get_width() - camera_width)
    bre = ((camera_height, camera_width))

    
    image = rc_utils.crop(image, tli, bre)
    ImageDepth = rc_utils.crop(ImageDepth, tli, bre)

    # Update contours based on color image
    contour, color = update_contours(image)

    
    image_display = np.copy(image)
    # Process contours if available
    if contour is not None:
       
        contour_center = rc_utils.get_contour_center(contour)

       
        rc_utils.draw_contour(image_display, contour)
        rc_utils.draw_circle(image_display, contour_center)

    
        distance = rc_utils.get_pixel_average_distance(ImageDepth, contour_center)
        last_dist = distance
        

    else:
        cur_state = State.search

    # Determine current state based on detected color
    if color == Color.RED:
        cur_state = State.red
        color_priority = Color.RED
    elif color == Color.BLUE:
        cur_state = State.blue
        color_priority = Color.BLUE
    elif color == Color.BOTH:
        cur_state = State.linear
    else:
        cur_state = State.search

    # Update car behavior based on current state
    match cur_state:
        
        case State.red:
            if cur_state == State.red and (distance < dist_param):
                angle = rc_utils.remap_range(contour_center[1], 0, camera_width, 0.3, 1)
                angle *= rc_utils.remap_range(last_dist, 200, 50, 0, 2)
                print("Angle:", angle)
                counter = 0
            elif cur_state == State.blue and (distance < dist_param):
                angle = rc_utils.remap_range(contour_center[1], 0, camera_width, -1, -0.3)
                angle *= rc_utils.remap_range(last_dist, 50, 200, 2, 0)
                print("Angle_Blue:", angle)
                counter = 0
            elif (cur_state == State.blue or cur_state == State.red) and distance >= dist_param:
                if cur_state == State.blue:
                    angle = rc_utils.remap_range(contour_center[1], 0, camera_width, -1, 1)
                elif cur_state == State.red:
                    angle = rc_utils.remap_range(contour_center[1], 0, camera_width, -1, 1)
                counter = 0
            elif cur_state == State.linear:
                angle = 0
                counter = 0
            else:
                if color_priority == Color.RED:
                    angle = rc_utils.remap_range(last_dist, 0, 100, -0.3, -0.68) 
                else:
                    angle = rc_utils.remap_range(last_dist, 0, 100, 0.3, 0.68)

        case State.blue:
            if cur_state == State.red and (distance < dist_param):
                angle = rc_utils.remap_range(contour_center[1], 0, camera_width, 0.3, 1)
                angle *= rc_utils.remap_range(last_dist, 200, 50, 0, 2)
                print("Angle:", angle)
                counter = 0
            elif cur_state == State.blue and (distance < dist_param):
                angle = rc_utils.remap_range(contour_center[1], 0, camera_width, -1, -0.3)
                angle *= rc_utils.remap_range(last_dist, 50, 200, 2, 0)
                print("Angle_Blue:", angle)
                counter = 0
            elif (cur_state == State.blue or cur_state == State.red) and distance >= dist_param:
                if cur_state == State.blue:
                    angle = rc_utils.remap_range(contour_center[1], 0, camera_width, -1, 1)
                elif cur_state == State.red:
                    angle = rc_utils.remap_range(contour_center[1], 0, camera_width, -1, 1)
                counter = 0
            elif cur_state == State.linear:
                angle = 0
                counter = 0
            else:
                if color_priority == Color.RED:
                    angle = rc_utils.remap_range(last_dist, 0, 100, -0.3, -0.68) 
                else:
                    angle = rc_utils.remap_range(last_dist, 0, 100, 0.3, 0.68)

        case State.search:
            if cur_state == State.red and (distance < dist_param):
                angle = rc_utils.remap_range(contour_center[1], 0, camera_width, 0.3, 1)
                angle *= rc_utils.remap_range(last_dist, 200, 50, 0, 2)
                print("Angle:", angle)
                counter = 0
            elif cur_state == State.blue and (distance < dist_param):
                angle = rc_utils.remap_range(contour_center[1], 0, camera_width, -1, -0.3)
                angle *= rc_utils.remap_range(last_dist, 50, 200, 2, 0)
                print("Angle_Blue:", angle)
                counter = 0
            elif (cur_state == State.blue or cur_state == State.red) and distance >= dist_param:
                if cur_state == State.blue:
                    angle = rc_utils.remap_range(contour_center[1], 0, camera_width, -1, 1)
                elif cur_state == State.red:
                    angle = rc_utils.remap_range(contour_center[1], 0, camera_width, -1, 1)
                counter = 0
            elif cur_state == State.linear:
                angle = 0
                counter = 0
            else:
                if color_priority == Color.RED:
                    angle = rc_utils.remap_range(last_dist, 0, 100, -0.3, -0.68) 
                else:
                    angle = rc_utils.remap_range(last_dist, 0, 100, 0.3, 0.68)
            


    # Clamping functions
    angle = rc_utils.clamp(angle, -1, 1)
    speed = 1
    speed = rc_utils.clamp(speed, -1, 1)
    
    print("cur_sate",cur_state)

    # Displaying the color camera that was drawn on
    rc.display.show_color_image(image_display)

    # Setting the speed and angle of the car
    rc.drive.set_speed_angle(speed, angle)

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()