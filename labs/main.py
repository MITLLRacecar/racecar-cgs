#importations
import ar_solver

color_input = None


#here we shall call our time trials
def update_LineFollowing(color_input):
	pass
def update_LaneFollowing():
	pass
def update_Slaloming():
	pass
def Walls():
	pass
###################################
potential_colors = [
    ((10, 50, 50), (20, 255, 255),), #orange
    ((100, 150, 50), (110, 255, 255)), #blue
    ((40, 50, 50), (80, 255, 255)),  # The HSV range for the color green
    ((170, 50, 50), (10, 255, 255)), #red
    ((110,59,50), (165,255,255),) #purple
]

Class States(Enum):
	"Idle" = 1
	"Line Following" = 2
	"Lane Following" = 3
	"Slaloming" = 4
	"Walls" = 5


#potential_colors = ar_solver.potential_colors

right_counter = 0
left_counter = 0

color = ""
state = ""

def start():
	state = "Idle"

def update():
	global state

	main()

	if state == 2:
		update_LineFollowing()
	elif state == 3:
		update_LaneFollowing()
	elif state == 4:
		update_Slaloming()
	elif state == 5:
		Walls()



def main():
	global state
	
	
	ar_markers = ar_solver.get_info()

	if len(ar_markers) != 0:
		if ar_markers[0] == "Follow the Red Line":
			color = potential_colors.red
			state = 2
		...
		elif ar_markers[0] == "Turn Left" and left_counter == 0:
			left_counter = 2
	if color is not None:
		return (color, 1)
	if color is None:
		return ()

"""
"Follow the RED Line"
"Follow the BLUE Line"
"Follow the GREEN Line"
"PURPLE Lane Following"
"ORANGE Lane Following"
"Slalom"
"Turn Left"
"Turn Right"
"""
