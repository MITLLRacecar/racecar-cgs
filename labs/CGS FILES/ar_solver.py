isSimulation = True
import math
import copy
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
import statistics
from nptyping import NDArray
from typing import Any, Tuple, List, Optional
from enum import Enum

# Import Racecar library
import sys
sys.path.append("../../library")
import racecar_core
import racecar_utils as rc_utils

rc = racecar_core.create_racecar(True)

potential_colors = [
    ((10, 50, 50), (20, 255, 255),'ORANGE'),
    ((100, 150, 50), (110, 255, 255),'BLUE'),
    ((40, 50, 50), (80, 255, 255),'GREEN'),  # The HSV range for the color green
    ((170, 50, 50), (10, 255, 255),'RED'),
    ((110,59,50), (165,255,255),'PURPLE')
]

class Orientation(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

class ARMarker:
    
    def __init__(self, marker_id, marker_corners):
        # TODO: Copy implementation from your previous ARMarker class
        self.__id = marker_id
        self.__corners = marker_corners
              
        if self.__corners[0][1] > self.__corners[2][1]:
            if self.__corners[0][0] > self.__corners[2][0]:
                self.__orientation = Orientation.DOWN
            else:
                self.__orientation = Orientation.RIGHT
        else:
            if self.__corners[0][0] > self.__corners[2][0]:
                self.__orientation = Orientation.LEFT
            else:
                self.__orientation = Orientation.UP
                
        # Create fields to store the detected color and the area of that color's contour
        self.__color = "not detected"
        self.__color_area = 0
        
    def detect_colors(self, image, potential_colors):
        # TODO: Copy the code we wrote previously to crop the image to the area around the ARMarker
        marker_top, marker_left = self.__corners[self.__orientation.value]
        marker_bottom, marker_right = self.__corners[(self.__orientation.value + 2) % 4]
        half_marker_height = (marker_bottom - marker_top) // 2
        half_marker_width = (marker_right - marker_left) // 2
        crop_top_left = (
            max(0, marker_top - half_marker_height),
            max(0, marker_left - half_marker_width),
        )
        crop_bottom_right = (
            min(image.shape[0], marker_bottom + half_marker_height) + 1,
            min(image.shape[1], marker_right + half_marker_width) + 1,
        )
        cropped_image = rc_utils.crop(image, crop_top_left, crop_bottom_right)
        
        # TODO: Copy the code we wrote previously to search for the colors in potential_colors
        for (hsv_lower, hsv_upper, color_name) in potential_colors:
            contours = rc_utils.find_contours(cropped_image, hsv_lower, hsv_upper) 
            largest_contour = rc_utils.get_largest_contour(contours)
            if largest_contour is not None:
                contour_area = rc_utils.get_contour_area(largest_contour)
                if contour_area > self.__color_area:
                    self.__color_area = contour_area
                    self.__color = color_name
            
    def get_id(self):
        # TODO: Copy implementation from your previous ARMarker class
        return self.__id
    
    
    def get_corners(self):
        # TODO: Copy implementation from your previous ARMarker class
        return self.__corners
    
    def get_orientation(self):
        # TODO: Copy implementation from your previous ARMarker class
        return self.__orientation
    
    def get_color(self):
        # TODO: Return the detected color
        return self.__color
    
    def __str__(self):
        # TODO: Update __str__ to include the ID, corners, and orientation, and color
        return f"ID: {self.__id}\nCorners: {self.__corners}\nOrientation: {self.__orientation}\nColor: {self.__color}"



def get_ar_markers(image):
    # Gather raw AR marker data from ArUco
    aruco_data = cv.aruco.detectMarkers(
        image,
        cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250),
        parameters=cv.aruco.DetectorParameters_create()
    )
    
    # A list of ARMarker objects representing the AR markers found in aruco_data
    markers = []
        
    for i in range(len(aruco_data[0])):
        # TODO: For each marker in aruco_data, extract the corners and id, change the corners into (row, col) format,
        # and create an ARMarker object with this data (see section 3.1)
        corners = aruco_data[0][i][0].astype(np.int32)
        for j in range(len(corners)):
            col = corners[j][0]
            corners[j][0] = corners[j][1]
            corners[j][1] = col
        marker_id = aruco_data[1][i][0]
        
        # TODO: Add the new marker to markers
        markers.append(ARMarker(marker_id, corners))
        markers[-1].detect_colors(image, potential_colors)
        
    return markers


def ar_info(marker: ARMarker):
    if marker.get_color() == 'PURPLE' or marker.get_color() == 'ORANGE':
        return f'{marker.get_color()} Lane Following'
    if marker.get_id() == 0:
        return 'Turn Left'
    if marker.get_id() == 1:
        return 'Turn Right'
    if marker.get_id() == 199:
        if marker.get_orientation() == Orientation.LEFT:
            return 'Turn Left'
        if marker.get_orientation() == Orientation.RIGHT:
            return 'Turn Right'
    if marker.get_id() == 2:
        if marker.get_color() == 'not detected':
            return 'Slalom'
        return f'Follow {marker.get_color()} line'

def get_markers_info():
    image = rc.camera.get_color_image_async()

    markers = get_ar_markers(image)
    msgs = []
    for i in markers:
	msgs.append(ar_info(i))
    return msgs
