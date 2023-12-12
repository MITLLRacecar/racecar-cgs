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
#from turtle import shape
from typing import Counter

sys.path.insert(1, "../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()
speed = 0
shapeConfig = 0
shapeCounter = 0

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
    global speed
    global isDrawing
    global shapeConfig
    global shapeCounter
    speed = 0
    isDrawing = False
    shapeConfig = 0
    shapeCounter = 0

    # Print start message
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
        "    Y button = drive in a right triangle"
    )


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    global shapeConfig
    global shapeCounter
    global isDrawing


    if not isDrawing:
        rc.drive.set_speed_angle(rc.controller.get_trigger(rc.controller.Trigger.RIGHT) - rc.controller.get_trigger(rc.controller.Trigger.LEFT), rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0])

    
        if rc.controller.was_pressed(rc.controller.Button.A):
            isDrawing = True
            print("Driving in a circle")
            shapeConfig = 1
            shapeCounter = 0
        
        elif rc.controller.was_pressed(rc.controller.Button.B):
            isDrawing = True
            print("Driving in a square")
            shapeConfig = 2
            shapeCounter = 0

        elif rc.controller.was_pressed(rc.controller.Button.X):
            isDrawing = True
            print("Driving in a figure 8")
            shapeConfig = 3
            shapeCounter = 0

        elif rc.controller.was_pressed(rc.controller.Button.Y):
            isDrawing = True
            print("Driving in a triangle")
            shapeConfig = 4
            shapeCounter = 0

    
    if rc.controller.was_pressed(rc.controller.Button.RB):
        isDrawing = False
    

    if isDrawing:
        if shapeConfig == 1:
            if shapeCounter < 6:
                rc.drive.set_speed_angle(1, 1)
            else:
                shapeCounter = 0
                isDrawing = False
                shapeConfig = 0
    
        elif shapeConfig == 2:
            if shapeCounter < 2:
                rc.drive.set_speed_angle(0.8, 0)
            elif shapeCounter < 4:
                rc.drive.set_speed_angle(0.6, 1)
            elif shapeCounter < 5:
                rc.drive.set_speed_angle(0.7, 0)
            elif shapeCounter < 7:
                rc.drive.set_speed_angle(0.6, 1)
            elif shapeCounter < 8:
                rc.drive.set_speed_angle(0.7, 0)
            elif shapeCounter < 10:
                rc.drive.set_speed_angle(0.5, 1)
            elif shapeCounter < 11:
                rc.drive.set_speed_angle(0.7, 0)
            elif shapeCounter < 13:
                rc.drive.set_speed_angle(0.5, 1)
            else:
                shapeCounter = 0
                isDrawing = False
                shapeConfig = 0
    
        elif shapeConfig == 3:
            if shapeCounter < 2:
                rc.drive.set_speed_angle(0.8, 0.1)
            elif shapeCounter < 3.5:
                rc.drive.set_speed_angle(0.9, 0.7)
            elif shapeCounter < 9:
                rc.drive.set_speed_angle(0.7, -0.9)
            elif shapeCounter < 11:
                rc.drive.set_speed_angle(1, 0.1)
            elif shapeCounter < 14:
                rc.drive.set_speed_angle(0.7, 0.9)
            if shapeCounter >= 18:
                shapeCounter = 0
                isDrawing = False
                shapeConfig = 0

        elif shapeConfig == 4:
            if shapeCounter < 2:
                rc.drive.set_speed_angle(1, 0)
            elif shapeCounter < 3:
                rc.drive.set_speed_angle(-0.5, -1)
            elif shapeCounter < 6:
                rc.drive.set_speed_angle(-1, 0)
            elif shapeCounter < 8:
                rc.drive.set_speed_angle(0.5, 1)
            elif shapeCounter < 12:
                rc.drive.set_speed_angle(1, 0)
            else:
                shapeCounter = 0
                isDrawing = False
                shapeConfig = 0
            
        shapeCounter += rc.get_delta_time()




########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()
