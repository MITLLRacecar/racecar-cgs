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

sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Put any global variables here
counter=0
circle_runtime=0###orfea edit this number. test it and make it work because i know that it is wrong
sq_counter=0
sq_strait=3###edit this
deg_90_time=1##this also
tr_count=0
tr_strait=3
deg_60_time=0.333333333#this also

########################################################################################
# Functions
########################################################################################


def start():
    """
    This function is run once every time the start button is pressed
    """
    # Begin at a full stop
    rc.drive.stop()

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


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    rc.drive.set_max_speed(1)
    # TODO (warmup): Implement acceleration and steering
    rc.drive.set_speed_angle(0, 0)

    if rc.controller.was_pressed(rc.controller.Button.A):
        print("Driving in a circle...")
        # TODO (main challenge): Drive in a circle
        while counter<circle_runtime:
            rc.drive.set_speed_angle(1, 0.5)###please orfea...test the angle!!! please sudo help
            counter=counter + rc.get_delta_time()###test this also
    else 
        counter=0
        if rc.controller.was_pressed(rc.controller.Button.B):
            print("Driving in square")
            while counter<4:
                while sq_counter<sq_strait:
                    rc.drive.set_speed_time(1, 0)
                    sq_counter=sq_counter+rc.get.delta_time()
                sq_counter=0
                while sq_counter<deg_90_time:
                    rc.drive.set_speed_angle(1, 1)
                    sq_counter=sq_counter+rc.get.delta_time()
                sq_counter=0
        else:
            if rc.controller.was_pressed(rc.controller.Button.X):
                print ("Driving in a 8")
                counter=0
                while counter<circle_runtime:
                    rc.drive.set_speed_angle(1, 0.5)###please orfea...test the angle!!! please sudo help
                    counter=counter + rc.get_delta_time()###test this also
                while counter<circle_runtime:
                    rc.drive.set_speed_angle(1, -0.5)###please orfea...test the angle!!! please sudo help
                    counter=counter + rc.get_delta_time()###test this also
            else:
                if rc.controller.was_pressed(rc.controller.Button.Y):
                    print("Driving in a triangle")
                    counter=0
                    while counter<3:
                        while tr_count<tr_strait:
                            rc.drive.set_speed_time(1, 0)
                            tr_count=tr_count+rc.get.delta_time()
                        tr_count=0
                        while tr_count<deg_60_time:
                            rc.drive.set_speed_angle(1, 1)
                            tr_count=tr_count+rc.get.delta_time()
                        tr_count=0
                        counter=counter+1

            # TODO (main challenge): Drive in a square when the B button is pressed

    # TODO (main challenge): Drive in a figure eight when the X button is pressed

    # TODO (main challenge): Drive in a shape of your choice when the Y button
    # is pressed


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()