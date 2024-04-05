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

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()


pureLogic = True
targetColor = ""

minContourArea = 10

croppingMin = (0, 0)
croppingMax = (rc.camera.get_height(), rc.camera.get_width())

COLOR = ((0, 0, 0), (0, 0, 0))
PURPLE = ((110,59,50), (165,255,255))
ORANGE = ((10, 50, 50), (20, 255, 255))

ORANGE_contours = [None, None]
PURPLE_contours = [None, None]

avg_contour_center = None


########################################################################################
# Functions
########################################################################################



def listRemove(multidimensional_list, list_to_remove):
    for index, sublist in enumerate(multidimensional_list):
        if np.array_equal(sublist, list_to_remove):
            del multidimensional_list[index]
            return multidimensional_list



def runLaneFollowing(target_color):
    global speed
    global angle
    global targetColor

    targetColor = target_color


    update_contour()


    angle = 0
    speed = 0

    if avg_contour_center is not None:

        angle = 2 * avg_contour_center[1] - rc.camera.get_width()
        angle /= rc.camera.get_width()

        speed = -avg_contour_center[0] + rc.camera.get_height() * 3 // 4
        speed /= rc.camera.get_height() // 4
        
    if speed < -1:
        speed = -1
    elif speed > 1:
        speed = 1
    if angle < -1:
        angle = -1
    elif angle > 1:
        angle = 1


    #rc.drive.set_speed_angle(speed, angle)
    rc.drive.set_speed_angle(rc.controller.get_trigger(rc.controller.Trigger.RIGHT) - rc.controller.get_trigger(rc.controller.Trigger.LEFT), rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0])

    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)




def computeAvg(Contours):
    
    global avg_contour_center
    
    if len(Contours) == 1:
                       
        center = rc_utils.get_contour_center(Contours[0])

        if center[1] < rc.camera.get_width() / 2:
            avg_contour_center = (center[0], (rc.camera.get_width() + center[1]) // 2)

        else:
            avg_contour_center = (center[0], center[1] // 2)
        
    else:
        center_1 = rc_utils.get_contour_center(Contours[0])
        center_2 = rc_utils.get_contour_center(Contours[1])
        print(center_1[0])
        print(center_2[0])
        avg_contour_center = ((center_1[0] + center_2[0]) // 2, (center_1[1] + center_2[1]) // 2)



def update_contour():
    
    global avg_contour_center
    global ORANGE
    global PURPLE
    global ORANGE_contours
    global PURPLE_contours
    global minContourArea


    ORANGE_contours = [None, None]
    PURPLE_contours = [None, None]

    image = rc.camera.get_color_image()


    if image is None:
        avg_contour_center = None
        
    else:
        image = rc_utils.crop(image, croppingMin, croppingMax)

        ORANGE_contourlist = list(rc_utils.find_contours(image, ORANGE[0], ORANGE[1]))
        PURPLE_contourlist = list(rc_utils.find_contours(image, PURPLE[0], PURPLE[1]))


        if ORANGE_contourlist is not None:
            ORANGE_contours[0] = rc_utils.get_largest_contour(ORANGE_contourlist, minContourArea)
            PURPLE_contourlist = listRemove(PURPLE_contourlist, PURPLE_contours[0])

            if len(ORANGE_contourlist) != 0:
                ORANGE_contours[1] = rc_utils.get_largest_contour(ORANGE_contourlist, minContourArea)


        if PURPLE_contourlist is not None:
            PURPLE_contours[0] = rc_utils.get_largest_contour(PURPLE_contourlist, minContourArea)
            PURPLE_contourlist = listRemove(PURPLE_contourlist, PURPLE_contours[0])

            if len(PURPLE_contourlist) != 0:
                PURPLE_contours[1] = rc_utils.get_largest_contour(PURPLE_contourlist, minContourArea)


        if PURPLE_contours is not [None, None] or ORANGE_contours is not [None, None]:
            
            print("OR: ", ORANGE_contours)
            print("PUR:", PURPLE_contours)

            if pureLogic:

                rc.display.show_color_image(image)
                """
                if targetColor == "ORANGE":
                    if not ORANGE_contours == [None, None]:
                        print("o")
                        computeAvg(ORANGE_contours)
                    else:
                        print("p'")
                        computeAvg(PURPLE_contours)
                
                else:
                    if not PURPLE_contours == [None, None]:
                        print("p")
                        computeAvg(PURPLE_contours)
                    else:
                        print("o'")
                        computeAvg(ORANGE_contours)"""


            else:
                contourNum = 0
                avg_contour_center = (0, 0)

                if PURPLE_contours != [None, None]:
                    for contour in PURPLE_contours:
                        contourNum += 1
                        newCenter = rc_utils.get_contour_center(contour)
                        avg_contour_center[0] += newCenter[0]
                        avg_contour_center[1] += newCenter[1]

                if ORANGE_contours != [None, None]:
                    for contour in ORANGE_contours:
                        contourNum += 1
                        newCenter = rc_utils.get_contour_center(contour)
                        avg_contour_center[0] += newCenter[0]
                        avg_contour_center[1] += newCenter[1]

                avg_contour_center[0] /= contourNum
                avg_contour_center[1] /= contourNum
        else:
            avg_contour_center = None




def start():
    print(
        "Time Trial - Line Following"
    )


def update():
    runLaneFollowing("Purple")




########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()
