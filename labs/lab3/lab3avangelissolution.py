# Import necessary libraries
from enum import IntEnum
import sys
import cv2 as cv
import numpy as np

# Insert the path to the library
sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils

# Create a Racecar object
rc = racecar_core.create_racecar()

# Initialize global variables
Cur_State_Distance = None
global Image_
global croped_image 
global Seccond_check
global left_box
global right_box 
global center_center   
global center_up

# Define an enumeration for distance states
class StateDistance(IntEnum):
    Too_close = 0
    OK = 1
    Too_Fast_and_close = 2
    Good = 3
    about_to_fall = 4

# Function to update depth image
def update_depth():
    global image
    global left_box
    global right_box 
    global center_center   
    global center_up
    image = rc.camera.get_depth_image()
    left_box = image
    right_box = image
    center_center = image
    center_up = image
    left_small = image

    # Crop different regions of the depth image
    image_croped = image
    left_box = rc_utils.crop(left_box , (190,0),(240,300) )
    right_box = rc_utils.crop(right_box , (190,425),(240,550) )
    center_center = rc_utils.crop(center_center , (190,270),(240,400) )
    center_up = rc_utils.crop(center_up , (210,280),(230,400) )
    left_small = rc_utils.crop(left_small , (230,0),(255,170) ) 
    rc.display.show_depth_image(left_small)

# Function to initialize the racecar and print controls
def start():
    rc.drive.stop()
    rc.set_update_slow_time(0.5)

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

# Function to update the racecar's state based on depth image and controls
def update():
    global Cur_State_Distance
    update_depth()
    
    # Get control inputs
    angle = rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0]
    rt = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    lt = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
    speed = rt - lt
    
    # Calculate distances to objects in different regions of the depth image
    pix_left_box_dist = rc_utils.get_closest_pixel(left_box,3)
    pix_right_box_dist = rc_utils.get_closest_pixel(right_box,3)
    pix_center_center_box_dist = rc_utils.get_closest_pixel(center_center,3)
    pix_center_up_box_dist = rc_utils.get_closest_pixel(center_up,3)
   
    left_box_dist = rc_utils.get_pixel_average_distance(left_box , pix_left_box_dist , 3)
    right_box_dist = rc_utils.get_pixel_average_distance(right_box , pix_right_box_dist , 3)
    center_center_box_dist = rc_utils.get_pixel_average_distance(center_center , pix_center_center_box_dist, 3)
    center_up_box_dist = rc_utils.get_pixel_average_distance(center_up , pix_center_up_box_dist , 3)

    # Calculate average distance in front of the car
    center_distance = (left_box_dist + right_box_dist + center_center_box_dist )/3

    # Handle cases where certain regions have no distance readings
    if center_center_box_dist == 0  and right_box_dist == 0:
        center_distance = left_box_dist
    if left_box_dist == 0 and right_box_dist == 0:
        center_distance = center_center_box_dist

    # Define distance thresholds
    Dist_clos = 38.6999999999999999999999999999999999
    Dist_far = 140
    Dist_max = 150

    # Determine distance state based on calculated distances
    if Dist_max > center_distance > Dist_far:
        Cur_State_Distance = StateDistance.Good
    elif Dist_clos <= center_distance <= Dist_far and speed < 0.16:
        Cur_State_Distance = StateDistance.OK
    elif Dist_clos <= center_distance <= Dist_far and speed > 0.16:
        Cur_State_Distance = StateDistance.Too_Fast_and_close
    elif center_distance < Dist_clos or center_distance == 0:
        Cur_State_Distance = StateDistance.Too_close

    # Act based on the determined distance state
    if Cur_State_Distance == StateDistance.Good or Cur_State_Distance == StateDistance.OK:
        rc.drive.set_speed_angle(speed, angle)
    elif Cur_State_Distance == StateDistance.Too_Fast_and_close:
        rc.drive.set_speed_angle(0.3, angle)
    elif Cur_State_Distance == StateDistance.Too_close:
        rc.drive.stop()

    # Additional actions based on specific conditions
    if center_distance > Dist_max or center_distance == 0:
        rc.drive.set_speed_angle(speed,angle)
    if center_center_box_dist == 0 and left_box_dist != 0 and right_box_dist != 0:
        rc.drive.set_speed_angle(1,0) 
    if 38.8123075861349 > center_up_box_dist > 37.67132 and Cur_State_Distance == StateDistance.Too_close:
        rc.drive.set_speed_angle(1,0) 

    # Print information on controller inputs
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle,"center distance", "distances", left_box_dist, right_box_dist , center_center_box_dist)
    if rc.controller.is_down(rc.controller.Button.B):
        print("Center distance:", center_distance, "StateDistance", Cur_State_Distance)

# Main execution loop
if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()

