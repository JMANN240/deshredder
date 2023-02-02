def basic(width, height=None):
	if height is None:
		height = width
	return list([list([1 for _ in range(width)]) for _ in range(height)])

h_lines = [
	[1,1,1,1,1],
	[1,1,1,1,1],
	[0,0,0,0,0],
	[-1,-1,-1,-1,-1],
	[-1,-1,-1,-1,-1],
]

v_lines = [
	[1,1,0,-1,-1],
	[1,1,0,-1,-1],
	[1,1,0,-1,-1],
	[1,1,0,-1,-1],
	[1,1,0,-1,-1],
]

