# Importations

import sys
import cv2 as cv
import numpy as np

import timetriallinefollowing as tt_Line

sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils
import ar_solver
from enum import Enum


# -- # -- # -- # -- # -- # -- # -- # -- # -- #
# -- # -- # -- # -- # -- # -- # -- # -- # -- #
# -- # -- # -- # -- # -- # -- # -- # -- # -- #


# Time trial functions from the guys.
# Here we shall call our time trials:
def update_LineFollowing(colorMin, colorMax):
	tt_Line.update_LineFollowing(colorMin, colorMax)
	
def update_LaneFollowing():
	pass

def update_Slaloming():
	pass

def update_WallFollowing():
	pass



# -- # -- # -- # -- # -- # -- # -- # -- # -- #
# -- # -- # -- # -- # -- # -- # -- # -- # -- #
# -- # -- # -- # -- # -- # -- # -- # -- # -- #



potential_colors = [
    ((10, 50, 50), (20, 255, 255),), # orange b
    ((100, 150, 50), (110, 255, 255)), # blue r
    ((40, 50, 50), (80, 255, 255)),  # green a
    ((170, 50, 50), (10, 255, 255)), # red i
    ((110,59,50), (165,255,255),) # purple n
]

class States(Enum):
	Idle = 1
	LineFollowing = 2
	LaneFollowing = 3
	Slaloming = 4
	Walls = 5
	TurnRight = 6
	TurnLeft = 7

right_counter = 0
left_counter = 0

color = ()
state = 1


# -- # -- # -- # -- # -- # -- # -- # -- # -- #
# -- # -- # -- # -- # -- # -- # -- # -- # -- #
# -- # -- # -- # -- # -- # -- # -- # -- # -- #



def start():
	global state
	global color

	state = 1
	color = potential_colors[1]


def update():
	global state
	global color

	if left_counter > 0:
		rc.drive.set_speed_angle(0.8, -0.8)
		left_counter -= rc.get_delta_time()
		return
	elif right_counter > 0:
		rc.drive.set_speed_angle(0.8, 0.8)
		right_counter -= rc.get_delta_time()
		return

	color_min = color[0]
	color_max = color[1]

	if state == 2:
		update_LineFollowing(color_min, color_max)
	elif state == 3:
		update_LaneFollowing(color_min, color_max)
	elif state == 4:
		update_Slaloming()
	elif state == 5:
		Walls()


def main():
	global state
	global color

	ar_markers = ar_solver.get_info()

	if len(ar_markers) != 0:
		if ar_markers[0] == "Follow the RED Line":
			color = potential_colors[3]
			state = 2
		elif ar_markers[0] == "Follow the GREEN Line":
			color = potential_colors[2]
			state = 2
		elif ar_markers[0] == "Follow the BLUE Line":
			color = potential_colors[1]
			state = 2
		elif ar_markers[0] == "ORANGE Lane Following":
			color = potential_colors[0]
			state = 3
		elif ar_markers[0] == "PURPLE Lane Following":
			color = potential_colors[4]
			state = 3
		elif ar_markers[0] == "Slalom":
			state = 4
		elif ar_markers[0] == "Turn Left":
			left_counter = 1
		elif ar_markers[0] == "Turn Right":
			right_counter = 1
		elif ar_markers[0] == "None":
			state = 5


"""
Les Messages
"Follow the RED Line"
"Follow the BLUE Line"
"Follow the GREEN Line"
"PURPLE Lane Following"
"ORANGE Lane Following"
"Slalom"
"Turn Left"
"Turn Right"
"""
"""
This is on a whole other level of f*ed up.
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣶⠶⠶⣶⣦⣄⠀⠀⠀⣀⣠⣤⣴⣶⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣶⠟⠋⠁⠀⠀⠀⠀⠀⠙⢷⣦⠟⠋⠉⠀⠀⠀⠈⠙⢿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⠋⠁⠀⢀⣤⠶⠚⠛⠛⠳⠶⣤⣙⣧⣀⠀⠀⣀⣀⣀⠀⠀⠙⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⡿⠁⠀⠀⠰⠋⠀⠀⠀⠀⣀⣠⣤⣬⣽⣿⣿⠉⠀⠀⠀⢈⣉⣉⣑⣊⣻⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⡿⠁⠀⠀⠀⠀⠀⣀⣴⠶⠛⠋⠉⠀⠀⠈⠉⠉⠻⣶⠶⠞⠛⠉⠉⠉⠉⠍⠛⠻⣇⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⡠⢋⠇⠀⠀⠀⠀⢰⠟⠋⠁⠀⠀⠀⠀⠀⣾⣿⣶⡆⠀⢻⡄⠀⠀⠀⠀⢸⣶⣶⣤⠀⠸⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣰⠞⠀⠀⠀⠀⠀⠀⠀⠸⠷⣶⣄⡀⠀⠀⠀⠀⠻⠿⠟⠀⢀⣼⠃⠀⠀⠀⠀⠘⠿⠾⠛⠀⣰⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣽⣷⣶⣤⣤⣤⣤⣶⣾⣿⡿⠛⠓⠲⠶⠶⠶⠖⠶⠾⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⣩⣿⠟⠋⠀⠀⠰⣦⣀⣀⣀⣀⣠⣴⡟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⠛⠉⠀⠀⠀⠀⠀⠀⠈⠻⣇⠀⠀⠀⠹⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣯⣤⣤⣤⣤⣾⣿⣤⣤⣀⡀⠀⠀⢀⣀⣤⣤⣀⣀⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡶⢿⡛⠛⠛⠷⠶⣤⣤⣀⣀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⡁⠀⠀⠀⠈⢻⣄⣀⡀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣟⣀⠘⠛⠛⠳⠶⠦⠤⣬⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠉⠉⠙
⡆⠀⠀⠀⠀⠀⠀⢶⣌⠛⠿⠿⠛⠻⠶⠶⣤⣾⣿⣿⣿⣿⣿⣿⣿⠟⠛⠛⠛⠋⠉⣉⣿⠟⠉⠉⣿⠿⢿⣿⡇⠀⠀⠀⠀⢀⡖⠀⠀⠀
⣿⣦⣀⠀⠀⠀⠀⠀⠉⠛⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⠿⠋⠁⠀⠉⠉⣉⣽⡿⠟⠋⠀⠀⠀⢠⣿⠀⢀⡿⠀⠀⠀⠀⢠⡞⠀⠀⠀⠀
⠈⠻⢿⣿⣿⣓⡶⠶⢤⣄⣀⣀⠀⣰⣿⣿⣿⣿⣿⡟⠁⠀⠀⣀⣤⣶⡾⠛⠁⠀⠀⠀⠀⠀⠀⠘⣿⠀⠈⠷⡀⠀⣠⠶⠋⠀⠀⠀⣠⠞
⠀⠀⠀⠈⠉⠛⠻⠿⠷⣶⣾⣿⣿⣿⣿⣿⣿⣿⣯⣭⣵⡶⠿⢛⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⠷⣦⣄⠉⠻⣇⠀⠀⠀⣠⠞⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⣿⣿⣿⣿⣿⡟⠉⠉⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡴⠟⠓⣶⠋⠁⠀⠀⣀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠘⠓⠳⣾⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⠁⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠿⠿⢿⣿⠿⠿⢿⢿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⠿⠿⠿⠿⣿⣿⣿



⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠈⠈⠉⠉⠈⠈⠈⠉⠉⠉⠉⠉⠉⠉⠉⠙⠻⣄⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⣄⠀⠀⢀⠀⢀⣀⣤⠄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⣉⣩⣤⠴⠶⠶⠒⠛⠛⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣴⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣧⠤⠶⠒⠚⠋⠉⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣾⡍⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣫⣭⣷⠶⢶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠶⠶⠖⠚⠛⠛⣹⠏⠀⠀⠀⠀⠀⠀⠀⠀⠴⠛⠛⠉⡁⠀⠀⠙⠻⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⡷⠷⢿⣦⣤⣈⡙⢿⣿⢆⣴⣤⡄⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣠⣤⡀⣸⡄⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⣿⣟⣩⣤⣴⣤⣌⣿⣿⣿⣦⣹⣿⢁⣿⣿⣄⣀⡀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢠⣿⠋⠻⢿⡁⠀⠀⠀⠀⠀⠀⠀⠀⢸⡿⠿⠛⢦⣽⣿⣿⢻⣿⣿⣿⣿⠋⠁⠘⣿⣿⣿⣿⣿⣿⣼⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⣿⠁⠀⠀⠙⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠿⣿⣯⣼⣿⡿⠟⠃⠀⠀⠀⣿⣿⣿⣿⣿⡛⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⣧⣴⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣺⠟⠃⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⢁⣀⣀⣀⣀⣀⣠⣀⣀⢀⢀⢀
⠀⠀⢿⠿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⡆⠙⠛⠛⠙⢻⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⡇⠀⠘⠃⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⡟⢿⣿⣆⠀⣸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢄⡼⠁⢀⣀⡀⠀⠀⠀⣦⣄⠀⣠⡄⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣷⣬⢻⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⣰⣿⡿⠿⠦⢤⣴⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠛⠛⠒⣿⣿⣿⡿⠟⠹⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡖⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⡿⣾⣿⣸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣆⣀⣀⣤⣴⣶⣶⣾⣿⣷⣦⣴⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⡇⣿⣿⡛⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢾⡟⠛⠛⠻⠛⠛⠛⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠓⢁⣬⣿⠇⠀⠀⠀⠀⠀⢠⡀⠀⠀⠀⠀⠀⢰⡿⣻⠇⠀⠀⠀⠀⠀⣠⣶⣶⣶⣶⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢐⣯⠞⠁⠀⠀⠀⠀⠀⠀⣄⠱⣄⠀⠀⠀⠀⠸⡧⠟⠆⠀⠀⠀⠀⠘⠿⢿⠿⠿⣿⡿⣿⠃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⡾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠘⢦⡈⠂⠀⠑⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢠⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠒⡄⠀⠀⠑⠄⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣦⣦⣼⡏⠳⣜⢿⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⢠⣷⣦⣤⣀⣀⣀⣴⣿⣿⣿⣿⣿⡿⠻⠆⠸⣎⣧⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣄⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣠⡄⠀⣿⢹⡇⢸⡀⠀⠈⠻⢿⣿⣿⣿⣿⣿⣿


⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⢿⣿⣟⡿⣿⣿⣻⡿⣟⣿⢿
⣿⣿⣿⣿⣿⣿⣿⣯⣿⢶⣣⡟⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣻⣿⣯⣿⣷⣿⣿⣿⣟⣿⣟⣿⡿⣾⣿⣟⣾⣿⣳⣿⣻⣽⢾⣻⣽⡿⣽⣻
⣿⣿⣿⣿⣿⣿⣿⣿⡿⣏⡷⣻⢮⣻⣿⣿⣟⣯⣿⣟⣿⣽⣿⣷⣿⣿⡿⣿⣻⣯⣿⣿⢿⣿⣽⣿⢿⣾⣿⣳⣿⣳⣟⣯⡿⢿⠟⣿⣽⢯
⣿⣿⣿⣿⣿⣻⣿⣿⣿⢽⡳⣝⢮⠷⣯⣿⣿⣿⣿⣟⣿⣿⣳⣿⣯⣿⣿⢿⣟⣿⣟⣿⣿⣯⣿⣾⣿⣟⣾⣟⣷⣿⠟⣭⡻⣭⢻⡜⣿⣿
⣿⣿⣿⣿⣽⣿⣿⣿⢿⡷⡽⣌⡳⢫⢽⣞⢿⣿⣿⣿⣻⣾⣿⣿⡿⣷⣿⣟⣿⣻⣿⣻⣾⣯⣷⣿⣿⣾⣿⣿⣻⣾⢫⡳⣝⢮⡳⣭⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢯⣷⡝⢦⡙⡗⣎⠿⣯⡟⣿⣿⣿⣿⣯⣷⣿⣿⣿⣾⣟⣿⣷⣿⣳⢿⣿⣿⣽⣾⣿⣿⡻⢬⡇⣟⡼⣣⢟⡴⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣞⣻⣯⢳⡹⡜⣥⠛⡴⢉⠆⣡⠃⢤⠉⠋⠍⡙⠋⡿⢟⣻⣿⣿⣿⣿⣿⣯⣷⣿⣟⢶⣙⠶⣙⢦⡝⡧⢏⡶⣿⢿
⣿⣿⣿⣾⣿⣿⣿⣿⣿⣎⣻⠣⡕⡜⣤⢋⣴⢫⡞⠟⡘⠉⠀⠄⡀⠄⡁⢀⠠⠙⣿⣿⣿⣿⣿⣿⣿⣿⣟⡮⡵⢫⣝⡺⡜⡭⣓⣾⣿⢿
⣿⣿⣿⣿⢿⣿⣿⣿⠿⣟⡻⠗⡞⡴⢎⡧⢚⠃⡐⠤⠒⠠⢁⠠⠀⠄⠠⠀⠄⠀⡉⠻⡟⣿⣿⣿⣿⣿⣾⢿⣝⣳⢎⡷⣙⠲⣭⣿⣻⣟
⣿⣿⣿⣿⣿⣿⣿⣿⡿⢹⢇⠻⣜⣱⢫⣼⣷⣦⣁⠆⢁⠂⠄⢀⠠⠀⠠⠀⠂⡐⠠⠡⠘⠤⣿⣿⣿⣿⣿⣿⡾⣥⢏⡶⣍⢳⣿⡽⣳⢾
⣿⣿⣿⣿⣿⣿⣿⠛⡠⢃⡜⠛⣾⣷⣿⣿⣿⣿⣿⣎⡆⡘⡐⠠⠀⡐⠀⢠⠑⡰⢀⣅⣧⣶⣶⣿⣿⣿⣿⣿⣿⣷⣋⠶⢭⣓⣯⢿⣽⣻
⣿⣿⣿⣟⣿⡿⢀⠣⡜⢡⠂⡁⢼⣿⣿⣿⣿⣿⣿⣿⠃⡐⣁⠂⡡⠀⢌⠢⡑⢢⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣍⡚⣔⣾⣯⢿⣞⡷
⣿⣿⣿⣿⣿⢅⠫⡔⢩⠂⠥⡀⠄⠙⠛⠿⠿⠿⢿⠿⡁⢆⠡⢊⠄⠣⢌⢢⠁⢾⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⠳⢏⡛⢮⡙
⣿⣿⣿⣿⣿⣊⠵⣌⠣⡍⢆⡱⢈⠔⠠⢀⢂⠱⢈⠰⢡⢎⢒⢳⡿⢿⣆⠦⡙⡜⢻⠛⠻⠿⠿⠿⠛⣡⣿⣻⣿⣿⣿⣿⣿⣇⠎⡜⡰⢌
⣿⣿⣿⣿⣿⡜⡲⣌⠳⣜⠣⡜⢡⢊⡕⢊⡔⣈⢲⣿⣟⣟⣜⣢⡙⢦⣻⣿⣦⣕⢂⠩⡐⡀⢄⡠⠐⢀⠸⠹⠿⣹⣿⣿⣿⣿⠰⣁⠆⢣
⣿⣿⣿⣾⣿⣇⡳⣌⡟⡴⣋⠼⣡⠖⣬⠣⣔⢂⢆⡩⢻⢿⣯⣽⣹⢿⣿⠿⠛⡋⢄⢣⡑⣉⠆⣉⠹⣦⡢⢑⠧⡀⠿⣿⣿⣿⡁⠆⡘⠄
⣿⣿⣻⣿⣿⠼⡱⢎⡼⣳⢭⣞⡵⣫⢶⡳⣬⢋⡶⣡⢷⣫⣿⣿⢞⡟⣧⣎⡱⠜⣆⠲⡜⡤⢓⡌⢣⠜⣿⣎⡒⠡⢌⣹⣿⡟⢀⠂⡐⠈
⣿⣿⣿⡿⣿⣭⢳⢏⡾⣱⢏⡾⣱⢿⣿⢿⡿⣿⣷⣿⣷⣷⣯⣿⣾⣽⣶⣎⡷⣹⢦⣛⡼⣺⠷⣾⣕⢮⡙⡟⢮⠑⡂⠄⢂⠌⠀⡐⠀⠄
⣿⣿⣿⣿⣿⣧⢛⣮⢳⡝⣮⡝⣧⡻⣜⢯⡻⣭⢻⡝⣯⢽⡯⢿⡽⢯⡿⣿⢿⡿⣿⢿⡿⣷⣻⡼⣻⢎⢷⣉⠦⡑⠌⡒⠤⠈⠀⡀⠠⠀
⣿⣿⣿⡿⣿⣧⢻⡬⣳⢝⣦⣛⠶⣽⡹⣎⢷⡭⢷⡹⣎⢷⡹⢧⡻⣭⢳⡝⣮⣳⠽⡾⣽⢳⢧⡻⡵⣚⢎⡞⢦⡑⢌⠰⠠⢁⠠⠀⠀⠀
⣿⣿⣿⣿⣿⢣⢻⡴⣫⢞⡴⣭⢺⣕⡻⣜⢧⣛⢧⡟⣼⢧⣛⣯⢳⡭⣷⡽⣳⢯⠿⣝⡞⣯⣳⢽⡱⢏⡞⣜⠣⡜⠠⢃⠂⡀⠀⢀⠂⠀
⣿⣿⣿⣿⣿⠭⢶⡹⣵⢫⡖⣧⢳⠮⡵⣋⠾⣭⢞⡽⣎⢷⣫⣞⢷⣻⡼⣽⢯⣯⢟⣽⣚⣧⡛⢮⡱⢫⡜⢤⠓⡌⢅⠂⡐⠀⠀⠠⠀⠀
⣿⣿⣿⣿⣯⢞⣣⠳⣜⢧⡻⣜⢧⡻⣕⣫⡝⣞⢮⡳⣝⢮⡳⣭⣛⢮⡽⣭⢳⣎⢿⡸⡱⢎⡙⢦⣉⠧⣘⠢⡑⣈⠂⢀⠀⠀⠈⠐⠀⠀
⣿⣿⣿⣿⣿⣧⢧⡛⣜⢎⡷⣹⢎⡷⣹⢶⡹⣎⢷⡹⣎⢷⡹⢶⣭⢳⡝⣮⢳⢎⣳⢳⣙⢮⡙⢆⢣⢒⡡⢒⠡⠂⠄⠂⢈⠀⠀⢈⠀⠀
⣿⣿⣿⣿⣿⣿⣶⣝⡺⡜⡼⣡⢟⡼⢣⡞⡵⢫⡞⡵⢫⡞⡽⣳⢎⡟⣾⡱⣏⡻⣜⡣⢏⡖⡹⢊⠳⡘⠰⠉⠂⠉⠀⠂⠄⠂⠀⠘⠀⠀




"""
