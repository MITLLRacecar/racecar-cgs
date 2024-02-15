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
import math

sys.path.insert(1, "../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Put any global variables here

global ssatElapsed
global ssatStack

ssatStack = [[0,0,0]]
ssatElapsed = 0
########################################################################################
# Functions
########################################################################################

def ssat(speed,angle,time):
    global ssatElapsed
    global ssatStack

    ssatStack.append([speed, angle, time])
    ssatElapsed = 0

def ssatUpdate():
    global ssatElapsed
    global ssatStack
    print(ssatStack)
    if ssatElapsed >= ssatStack[0][2]:
        ssatStack.pop(0)
        if len(ssatStack) == 0:
            ssatStack.append([0,0,0])
        else:
            ssatElapsed = 0
        rc.drive.stop()
    rc.drive.set_speed_angle(ssatStack[0][0], ssatStack[0][1])
    ssatElapsed += rc.get_delta_time()

def ssatStop():
    global ssatStack

    ssatStack = [[0,0,0]]

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

    global shapingSomething
    global shapeTimeElapsed
    global shapeTimeEnd

    shapingSomething = False
    shapeTimeElapsed = 0
    shapeTimeEnd = 0
    
    ssatStop()

def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    
    ssatUpdate()

    global shapingSomething

    #acceleration and steering
    if rc.controller.get_trigger(rc.controller.Trigger.RIGHT):
        ssatStop()
        ssat(1, rc.controller.get_joystick(rc.controller.Joystick(0))[0], math.inf)
    if rc.controller.get_trigger(rc.controller.Trigger.LEFT):
        ssatStop()
        ssat(-1, rc.controller.get_joystick(rc.controller.Joystick(0))[0], math.inf)

    if rc.controller.was_pressed(rc.controller.Button.A):
        ssatStop()
        ssat(1,1,5)
        # TODO (main challenge): Drive in a circle

    # TODO (main challenge): Drive in a square when the B button is pressed
    if rc.controller.was_pressed(rc.controller.Button.B):
        ssatStop()
        ssat(1,0,1)
        ssat(1,1,1.4)
        ssat(1,0,0.8)
        ssat(1,1,1.4)
        ssat(1,0,0.5)
        ssat(1,1,1.4)
        ssat(1,0,0.5)
        ssat(1,1,0.4)

    # TODO (main challenge): Drive in a figure eight when the X button is pressed
    if rc.controller.was_pressed(rc.controller.Button.X):
        ssatStop()
        ssat(1,0,3)
        ssat(1,1,3.5)
        ssat(1,0,2.4)
        ssat(1,-1,2.7)
    # TODO (main challenge): Drive in a shape of your choice when the Y button
    if rc.controller.was_pressed(rc.controller.Button.Y):
        ssatStop()
        ssat(1,1,2.4)
        ssat(1,1,2.4)
    # is pressed


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()
