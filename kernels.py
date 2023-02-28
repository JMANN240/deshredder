#
# Generator function to make a square or rectangular kernel of all 1s
#
def basic(width, height=None):
	if height is None:
		height = width
	return list([list([1 for _ in range(width)]) for _ in range(height)])


#
# A pre-made kernel to detect horizontal lines
#
h_lines = [
	[1,1,1,1,1],
	[1,1,1,1,1],
	[0,0,0,0,0],
	[-1,-1,-1,-1,-1],
	[-1,-1,-1,-1,-1],
]


#
# A pre-made kernel to detect vertical lines
#
v_lines = [
	[1,1,0,-1,-1],
	[1,1,0,-1,-1],
	[1,1,0,-1,-1],
	[1,1,0,-1,-1],
	[1,1,0,-1,-1],
]

