"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 1 - Driving in Shapes
"""

########################################################################################
# Imports
########################################################################################

import sys

from typing import Counter

sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Put any global variables here

########################################################################################
# Functions
########################################################################################

def start():
    """
    This function is run once every time the start button is pressed
    """
    # Begin at a full stop
    rc.drive.stop()

    global Counter, isDriving
    isDriving = False
    Counter = 0
    circle_started = False
  
    global isDriving1
    global isDriving2
    global isDriving3
    isDriving1 = False
    isDriving2 = False
    isDriving3 = False

    # Print start message
    # TODO (main challenge): add a line explaining what the Y button does
    print(
        ">> Lab 1 - Driving in Shapes\n"
        "\n"
        "Controls:\n"
        "    Right trigger = accelerate forward\n"
        "    Left trigger = accelerate backward\n"
        "    Left joystick = turn front wheels\n"
        "    A button = drive in a circle\n"
        "    B button = drive in a square\n"
        "    X button = drive in a figure eight\n"
    )

    global right_trigger_value, left_trigger_value, left_joystick_value
    global turn_scale, turn_angle, left_wheel_speed, right_wheel_speed
    figure_eight_started = False

def update():
    global Counter
    global isDriving
    global isDriving1
    global isDriving2
    global isDriving3

    SPEED_NORMAL = 1.0
    SPEED_SQUARE = 0.5
    SPEED_FIGURE_EIGHT = 0.5
    TURNING_NORMAL = 1.0
    TURNING_SQUARE = 1.0
    TURNING_FIGURE_EIGHT = -1.0

    left_joystick_value = rc.controller.get_joystick(rc.controller.Joystick.LEFT)
    
    # Extract the x-value for turning
    turning_value = left_joystick_value[0]
    # Check the right trigger value
    right_trigger_value = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)

    # Check if the right trigger is pressed
    if right_trigger_value > 0:
        # Drive forward with speed based on the right trigger position
        rc.drive.set_speed_angle(right_trigger_value, turning_value)
        return  
    else:
        # Decrease speed gradually if the trigger is released
        current_speed = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
        if current_speed > 0:
            new_speed = max(0, current_speed - rc.get_delta_time())
            rc.drive.set_speed_angle(new_speed, turning_value)
        else:
            # If the speed is already zero, stop the car
            rc.drive.stop()
    
    # Check the left trigger value
    left_trigger_value = rc.controller.get_trigger(rc.controller.Trigger.LEFT)

    # Check if the left trigger is pressed
    if left_trigger_value > 0:
        # Drive backward with speed based on the left trigger position
        rc.drive.set_speed_angle(-left_trigger_value, turning_value)  # Negative speed for backward motion
        return
    else:
        # Increase speed gradually if the trigger is released
        current_speed = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
        if current_speed > 0:
            new_speed = min(1, current_speed + rc.get_delta_time())  # Inverted and adjusted
            rc.drive.set_speed_angle(new_speed, turning_value)
        else:
            # If the speed is already zero, stop the car
            rc.drive.stop()
      
      # Check if the A button is pressed
    if rc.controller.was_pressed(rc.controller.Button.A) and not isDriving:
        isDriving = True  # Start driving in a circle
        Counter = 0  # Reset the counter

    # Check if the car should be driving in a circle
    if isDriving:
        Counter += rc.get_delta_time()

        # Drive in a clockwise circle
        speed = SPEED_NORMAL  # Adjust the speed as needed
        turning_value = TURNING_NORMAL  # Adjust the turning angle for clockwise motion
        

        # Drive for a certain duration (adjust as needed)
        if 0 <= Counter < 6.19:
            rc.drive.set_speed_angle(min(speed, 1.0), turning_value)
        elif 6.19 <= Counter < 6.40:
            rc.drive.set_speed_angle(min(-speed, -1.0), 0.0)
        elif Counter >= 6.41:
            rc.drive.stop()
            

    # Check if the B button is pressed
    if rc.controller.was_pressed(rc.controller.Button.B) and not isDriving1:
        isDriving1 = True  # Start driving in a square
        Counter = 0  # Reset the counter

    # Check if the car should be driving in a square
    if isDriving1:
        Counter += rc.get_delta_time()

        # Drive in a clockwise square
        speed = SPEED_SQUARE  # Adjust the speed as needed
        turning_value = TURNING_SQUARE  # Adjust the turning angle for clockwise motion

        # Switch between straight and turning segments based on time
        if 0 <= Counter < 3:
            rc.drive.set_speed_angle(min(speed, 1.0), 0.0)  # Drive straight for 2.5 seconds
        elif 3 <= Counter < 5.80:
            rc.drive.set_speed_angle(min(speed, 1.0), turning_value)  # Turn right for 1 second
        elif 5.80 <= Counter < 6.7:
            rc.drive.set_speed_angle(min(speed, 1.0), 0.0)
        elif 6.7 <= Counter < 8.4:
            rc.drive.set_speed_angle(min(speed, 1.0), turning_value) 
        elif 8.4 <= Counter < 9.4:
            rc.drive.set_speed_angle(min(speed, 1.0), 0.0) 
        elif 9.4 <= Counter < 12:
            rc.drive.set_speed_angle(min(speed, 1.0), turning_value)
        elif 12 <= Counter < 13:
            rc.drive.set_speed_angle(min(speed, 1.0), 0.0) 
        elif 13 <= Counter < 14.5:
            rc.drive.set_speed_angle(min(speed, 1.0), turning_value)
        elif Counter >= 1999:
                rc.drive.stop()
              # Stop driving in a square when the duration is reached

    # Check if the X button is pressed
    if rc.controller.was_pressed(rc.controller.Button.X) and not isDriving2:
        isDriving2 = True  # Start driving in a figure-eight
        Counter = 0  # Reset the counter

    # Check if the car should be driving in a figure-eight
    if isDriving2:
        Counter += rc.get_delta_time()

        # Drive in a figure-eight
        speed = SPEED_FIGURE_EIGHT  # Adjust the speed as needed
        turning_value = TURNING_FIGURE_EIGHT  # Adjust the turning angle for clockwise motion

        # Drive straight for 2 seconds, then turn right for 1 second, then turn left for 1 second, and repeat
        if 0 <= Counter < 6.0:
            rc.drive.set_speed_angle(min(speed, 1.0), 0.0)  # Drive straight
        elif 6.0 <= Counter < 12.66:
            rc.drive.set_speed_angle(min(speed, 1.0), -turning_value)
        elif 12.66 <= Counter < 16.33:
            rc.drive.set_speed_angle(min(speed, 1.0), 0.0)
        elif 16.33 <= Counter < 22.66:
            rc.drive.set_speed_angle(min(speed, 1.0), turning_value)   
        

    # Check if the Y button is pressed
    if rc.controller.was_pressed(rc.controller.Button.Y) and not isDriving3:
        isDriving3 = True  # Start driving in a circle
        Counter = 0  # Reset the counter

    # Check if the car should be driving in a circle
    if isDriving3:
        Counter += rc.get_delta_time()

        # Drive in a clockwise circle
        speed = SPEED_NORMAL  # Adjust the speed as needed
        turning_value = TURNING_NORMAL  # Adjust the turning angle for clockwise motion
        rc.drive.set_speed_angle(min(speed, 1.0), turning_value)

        # Drive for a certain duration (adjust as needed)
        if Counter > 15.00:
            rc.drive.stop()

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()