

def update_LineFollowing():
	pass






Class States(Enum):
	"Idle" = 1
	"Line Following" = 2
	"Lane Following" = 3
	"Slaloming"


potential_colors = ar_solver.potential_colors

right_counter = 0
left_counter = 0

color = ""
state = ""

def start():
	state = "Idle"

def update():
	global state

	main()

	if state = 2:
		update_LineFollowing()



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