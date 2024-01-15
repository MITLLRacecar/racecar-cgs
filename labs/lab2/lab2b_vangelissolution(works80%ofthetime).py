"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 2B - Color Image Cone Parking
"""

########################################################################################
# Imports
########################################################################################

from enum import IntEnum
import random
from re import search
import sys
from tracemalloc import stop
#from turtle import distance
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

# The HSV range for the color orange, stored as (hsv_min, hsv_max)
ORANGE = ((10, 100, 100), (20, 255, 255))

# >> Variables
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour
Stopping_distance = 30
global cur_state
########################################################################################
# Functions
########################################################################################


def update_contour():
    """
    Finds contours in the current color image and uses them to update contour_center
    and contour_area
    """
    global contour_center
    global contour_area
  
    
    
    image = rc.camera.get_color_image()
    

    if image is None:
        contour_center = None
        contour_area = 0
    

    else:
        # Find all of the orange contours
        contours = rc_utils.find_contours(image, ORANGE[0], ORANGE[1])

        # Select the largest contour
        contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA)

        if contour is not None:
            # Calculate contour information
            contour_center = rc_utils.get_contour_center(contour)
            contour_area = rc_utils.get_contour_area(contour)

            # Draw contour onto the image
            rc_utils.draw_contour(image, contour)
            rc_utils.draw_circle(image, contour_center)

        else:
            contour_center = None
            contour_area = 0


        
        # Display the image to the screen
        rc.display.show_color_image(image)


    #def update_depth():

    global Distance_cone
    global center_y
    global center_x
    
    imageDepth = rc.camera.get_depth_image()
    if contour_center is not None:
        center_y = contour_center[0]
        center_x = contour_center[1]
    elif rc_utils.get_contour_center(contour) is not None:
        center_y = rc_utils.get_contour_center(contour)[0]
        center_x = rc_utils.get_contour_center(contour)[1]

        
    if imageDepth is None:
        Distance_cone = 0
    else:
        Distance_cone = imageDepth[center_y][center_x]
        
        rc.display.show_depth_image(imageDepth)


def start():
    """
    This function is run once every time the start button is pressed
    """
    global speed
    global angle
    global Angle_error
    global random_angle
    global random_speed
    global cur_state
   

    Angle_error = 0
  
    cur_state = State.search
    random_speed = random.uniform(-1,1)
    random_angle = random.uniform(-1,1)
    # Initialize variables
    speed = 0
    angle = 0

    # Set initial driving speed and angle
    rc.drive.set_speed_angle(speed, angle)

    # Set update_slow to refresh every half second
    rc.set_update_slow_time(0.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)

    # Print start message
    print(">> Lab 2B - Color Image Cone Parking")
    
    

class State(IntEnum):

    search = 0
    approach = 1
    stoping = 2
    stop = 3
    too_far = 4


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """

    #TODO use state machines to make the car stop 30 cm away fro the cone 
    global speed
    global angle
    global Angle_error
    global cur_state
    global Speed_error
    #global center_y
    #global center_x

    #center_y = contour_center[0]
    #center_x = contour_center[1]

    
  
    Angle_error = 0
    Speed_error = 0

    #Angle_error = (contour_center[1] - 320) / 320
    #update_depth()

    update_contour()


    match cur_state:
        case State.search:
            if contour_center is None:
                rc.drive.set_speed_angle(random_speed,random_angle)
            else:
                cur_state = State.approach


        case State.approach:

            if Distance_cone > 100:
                speed = 0.6
            if Distance_cone > 100 and Distance_cone < 70:
                speed = 0.5
            if Distance_cone < 70 and Distance_cone > 46:
                speed = 0.7
            if Distance_cone > 46 :
                Angle_error = (contour_center[1] - 320) / 320
                angle = 0.5 * Angle_error
                rc.drive.set_speed_angle(speed,angle) 
            elif Distance_cone > 30:
                cur_state = State.stoping
            else:
                cur_state = State.stop

    
        case State.stoping:
            if Distance_cone > 37 and Distance_cone < 46 :
                rc.drive.set_speed_angle(-0.26,angle)
            elif Distance_cone > 45:
                cur_state = State.approach
            else:
                cur_state = State.stop

        case State.stop:
            if Distance_cone > 29.9 and Distance_cone < 30:
                rc.drive.set_speed_angle(0,0)
            elif Distance_cone < 29:
                cur_state = State.too_far
            elif Distance_cone > 31:
                cur_state = State.stoping
           

        case State.too_far: 
            if Distance_cone < 29:
                rc.drive.set_speed_angle(-0.6,0)
            elif Distance_cone > 29: 
                cur_state=State.stop

        case _: 
            print("error in match statment")
   # if contour_center is None:

     #   cur_state = State.search
     #   rc.drive.set_speed_angle(random_speed,random_angle)

   # if contour_center is not None:
    #    cur_state = State.approach

   # if cur_state == State.approach:
    #    Angle_error = (contour_center[1] - 320) / 320
     #   Speed_error = Distance_cone/900
      #  angle = 0.5 * Angle_error
       # speed = 0.8 
        #rc.drive.set_speed_angle(speed,angle) 

   # if Distance_cone < 40 and cur_state != State.stop:
    #    cur_state = State.stoping
     #   if cur_state == State.stoping:
      #      rc.drive.set_speed_angle(-0.8,0) 
       #     if Distance_cone < 32 and Distance_cone > 9  :
        #        cur_state = State.stoping
         #       if cur_state == State.stoping:
          #          rc.drive.set_speed_angle(0,0) 
           #         if Distance_cone < 29:
            #            cur_state = State.too_far
             #           rc.drive.set_speed_angle(-0.6,0)


    
     
        


    # Print the current speed and angle when the A button is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle,"cone distance",Distance_cone,"curent state",cur_state)

    # Print the center and area of the largest contour when B is held down
    if rc.controller.is_down(rc.controller.Button.B):
        if contour_center is None:
            print("No contour found")
        else:
            print("Center:", contour_center, "Area:", contour_area,"center y", center_y, "center x", center_x)#,"center y",center_y ,"center x", center_x,"distance cone", Distance_cone)


def update_slow():

    global random_speed
    global random_angle

    random_speed = random.uniform(-1,1)
    random_angle = random.uniform(-1,1)
    """
    After start() is run, this function is run at a constant rate that is slower
    than update().  By default, update_slow() is run once per second
    """
    # Print a line of ascii text denoting the contour area and x position
    if rc.camera.get_color_image() is None:
        # If no image is found, print all X's and don't display an image
        print("X" * 10 + " (No image) " + "X" * 10)
    else:
        # If an image is found but no contour is found, print all dashes
        if contour_center is None:
            print("-" * 32 + " : area = " + str(contour_area))

        # Otherwise, print a line of dashes with a | indicating the contour x-position
        else:
            s = ["-"] * 32
            s[int(contour_center[1] / 20)] = "|"
            print("".join(s) + " : area = " + str(contour_area))


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
