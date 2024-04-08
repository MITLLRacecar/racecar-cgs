# Importations

import sys
import cv2 as cv
import numpy as np
import math

sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils
import ar_solver
from enum import Enum


# -- # -- # -- # -- # -- # -- # -- # -- # -- #
# -- # -- # -- # -- # -- # -- # -- # -- # -- #
# -- # -- # -- # -- # -- # -- # -- # -- # -- #


# Time trial functions from the guys.
import TTLineFollowing as tt_Line
import TTLaneFollowing as tt_Lane
import TTWallFollowing as tt_Wall
import TTConeSlaloming as tt_Cone


# Here we shall call our time trials:
def updateLineFollowing():
	tt_Line.runLineFollowing(color)
	
def updateLaneFollowing():
	tt_Lane.runLaneFollowing(color)

def updateWallFollowing():
	tt_Wall.update()

def updateSlaloming():
	tt_Cone.update()



# -- # -- # -- # -- # -- # -- # -- # -- # -- #
# -- # -- # -- # -- # -- # -- # -- # -- # -- #
# -- # -- # -- # -- # -- # -- # -- # -- # -- #



# ~~~ # - # ~~~ # - # ~~~ # - # ~~~ # - # ~~~ # - # ~~~ #
# ~~~ # - # ~~~ # - # ~~~ # - # ~~~ # - # ~~~ # - # ~~~ #
# ~~~ # - #                                   # - # ~~~ #
					# It'll all turn out ok.
rc = racecar_core.create_racecar()            # - # ~~~ # Doesn't work? Boo-Hoo.
			# You're fine   	# You're ok.
# ~~~ # - #                                   # - # ~~~ #
# ~~~ # - # ~~~ # - # ~~~ # - # ~~~ # - # ~~~ # - # ~~~ #
# ~~~ # - # ~~~ # - # ~~~ # - # ~~~ # - # ~~~ # - # ~~~ #



potential_colors = [
    ("Orange", (10, 50, 50), (20, 255, 255)), # orange
    ("Blue", (100, 150, 50), (110, 255, 255)), # blue
    ("Green", (40, 50, 50), (80, 255, 255)),  # green
    ("Red", (170, 50, 50), (10, 255, 255)), # red
    ("Purple", (110,59,50), (165,255,255),) # purple
]

class states(Enum):
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

	tt_Line.setUp(rc)
	tt_Lane.setUp(rc)
	tt_Wall.setUp(rc)
	tt_Cone.setUp(rc)
	ar_solver.setUp(rc)
	tt_Line.start()
	tt_Lane.start()
	tt_Wall.start()
	tt_Cone.start()



def update():
	global state
	global color
	global left_counter
	global right_counter

	# We can run it here Yioupi!
	main()
	# And it doesn't create like 50 RaceCars!!!
	# Extra Yioupi!

	if left_counter > 0:
		rc.drive.set_speed_angle(0.8, -0.8)
		left_counter -= rc.get_delta_time()
		return
	
	elif right_counter > 0:
		rc.drive.set_speed_angle(0.8, 0.8)
		right_counter -= rc.get_delta_time()
		return


	if state == states.LineFollowing:
		updateLineFollowing()
	
	elif state == states.LaneFollowing:
		updateLaneFollowing()
	
	elif state == states.Slaloming:
		updateSlaloming()
	
	else:
		updateWallFollowing()

	if state != states.Walls:
		scan = rc.lidar.get_samples()
		lidar_closest_in_safety = rc_utils.get_lidar_closest_point(scan, (270,90))
		if lidar_closest_in_safety[1] < 60*math.sin(lidar_closest_in_safety[0]):
			if lidar_closest_in_safety[0] >= 270:
				rc.drive.set_speed_angle(-1, -0.5)
			else:
				rc.drive.set_speed_angle(-1, 0.5)
	else:
		scan = rc.lidar.get_samples()
		lidar_closest_in_safety = rc_utils.get_lidar_closest_point(scan, (270,90))
		if lidar_closest_in_safety[1] < 20*math.sin(lidar_closest_in_safety[0]):
			if lidar_closest_in_safety[0] >= 270:
				rc.drive.set_speed_angle(-1, -0.5)
			else:
				rc.drive.set_speed_angle(-1, 0.5)

	#rc.drive.set_speed_angle(rc.controller.get_trigger(rc.controller.Trigger.RIGHT) - rc.controller.get_trigger(rc.controller.Trigger.LEFT), rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0])



# -- # -- # -- # -- # -- # -- # -- # -- # -- #
# -- # -- # -- # -- # -- # -- # -- # -- # -- #
# -- # -- # -- # -- # -- # -- # -- # -- # -- #



def main():
	global state
	global color
	global left_counter
	global right_counter

	#ar_markers = ar_solver.get_markers_info()
	ar_markers = []
	#print(ar_markers)

	
	if len(ar_markers) != 0:
		
		if ar_markers[0] == "Follow the RED Line":
			color = potential_colors[3]
			state = states.LineFollowing
		elif ar_markers[0] == "Follow the GREEN Line":
			color = potential_colors[2]
			state = states.LineFollowing
		elif ar_markers[0] == "Follow the BLUE Line":
			color = potential_colors[1]
			state = states.LineFollowing

		elif ar_markers[0] == "ORANGE Lane Following":
			color = potential_colors[0]
			state = states.LaneFollowing
		elif ar_markers[0] == "PURPLE Lane Following":
			color = potential_colors[4]
			state = states.LaneFollowing
		
		elif ar_markers[0] == "Slalom":
			state = states.Slaloming
		
		elif ar_markers[0] == "Turn Left":
			left_counter = 1
		elif ar_markers[0] == "Turn Right":
			right_counter = 1
		
		else:
			state = states.Walls
		
	# """
	if rc.controller.was_pressed(rc.controller.Button.A):
		color = potential_colors[3][0]
		state = states.Walls
	elif rc.controller.was_pressed(rc.controller.Button.B):
		color = potential_colors[2][0]
		state = states.LineFollowing
	elif rc.controller.was_pressed(rc.controller.Button.X):
		color = potential_colors[1][0]
		state = states.LineFollowing

	elif rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0] == -1:
		color = potential_colors[0][0]
		state = states.LaneFollowing
	elif rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0] == 1:
		color = potential_colors[4][0]
		state = states.LaneFollowing
		
	elif rc.controller.was_pressed(rc.controller.Button.Y):
		state = states.Slaloming
		
	elif rc.controller.get_trigger(rc.controller.Trigger.LEFT) == 1:
		left_counter = 1
	elif rc.controller.get_trigger(rc.controller.Trigger.RIGHT) == 1:
		right_counter = 1
		
	elif rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0] == -1 and rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0] == 1:
		state = states.Walls
	# """
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



# -- # -- # -- # -- # -- # -- # -- # -- # -- #
# -- # -- # -- # -- # -- # -- # -- # -- # -- #
# -- # -- # -- # -- # -- # -- # -- # -- # -- #



if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
	
