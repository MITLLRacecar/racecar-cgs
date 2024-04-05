"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 2B - Color Image Cone Parking
"""

########################################################################################
# Imports
########################################################################################

import sys
import cv2 as cv
import numpy as np

sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils
import ar_solver

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# >> Constants
# The smallest contour we will recognize as a valid contour
MIN_CONTOUR_AREA = 30

possibleColors = {
    "Blue": ((100, 150, 50), (110, 255, 255)),
    "Green": ((40, 50, 50), (80, 255, 255)),
    "Red": ((170, 50, 50), (10, 255, 255)),
}


colorOrder = ["Red", "Green", "Blue"]


croppingMin = (320, 0)
croppingMax = (rc.camera.get_height(), rc.camera.get_width())

colorMin = (0, 0, 0)
colorMax = (0, 0, 0)

# >> Variables
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour

########################################################################################
# Functions
########################################################################################


def reorder(firstColor)
    colorOrder.remove(firstColor)
    colorOrder.insert(0, firstColor)



def runLineFollowing(colorToFollow):
    global speed
    global angle


    reorder(colorToFollow)

    
    # Search for contours in the current color image
    update_contour()
    
    if contour_center is not None:
        
        #now we shall go out of our way to find the angles
        angle = 2 * contour_center[1] - rc.camera.get_width()
        angle = angle / rc.camera.get_width()
        

    forwardSpeed = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    backSpeed = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
    speed = forwardSpeed - backSpeed

    rc.drive.set_speed_angle(speed, angle)



    # Print the current speed and angle when the A button is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # Print the center and area of the largest contour when B is held down
    if rc.controller.is_down(rc.controller.Button.B):
        if contour_center is None:
            print("No contour found")
        else:
            print("Center:", contour_center, "Area:", contour_area)




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
        # Crop the image to the floor directly in front of the car
        image = rc_utils.crop(image, CROP_FLOOR[0], CROP_FLOOR[1])

        contour = None

        for testingColor in colorOrder:
            contours = rc_utils.find_contours(image, possibleColors[testingColor][0], testingColor[testingColor][1])

            if contours:
                # Select the largest contour
                contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA)
                break    


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






def start():
    """
    This function is run once every time the start button is pressed
    """
    global speed
    global angle

    # Print start message
    print(
        "Line Following"
    )

def update():
    runLineFollowing()



########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()
