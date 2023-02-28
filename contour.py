import util

#
# Represents a closed-loop of white pixels
# Uses lazy loading
#
class Contour:
	def __init__(self, image):
		self.image = image
		self._stroke = None
		self._fill = None
		self._xs = None
		self._ys = None

	# Recursively find the group of white pixels adjacent to coordinate, return a list of all coordinates
	def _get_adjacent_whites(self, coordinate, list):
		list.append(coordinate)
		(x, y) = coordinate

		# We want to check each neighbor to see if they are white
		neighbor_coordinates = ((x-1, y), (x, y-1), (x+1, y), (x, y+1))
		for neighbor_coordinate in neighbor_coordinates:
			
			# If we are going to check a neighbor it must satisfy the following
			new_pixel = neighbor_coordinate not in list # Not already checked
			pixel_in_image = util.coordinate_in_bounds(self.image, neighbor_coordinate) # Not out of image bounds
			pixel_is_white = self.image.getpixel(neighbor_coordinate) == 255 # White

			# If it satisfies these conditions, check its neighbors
			if new_pixel and pixel_in_image and pixel_is_white:
				self._get_adjacent_whites(self.image, neighbor_coordinate, list)

		return list
	
	#
	# Represents the edge of a contour, returns a list of coordinates
	#
	def stroke(self):
		# Lazy loading
		if self._stroke is None:

			# Find first white pixel from the left of the image
			first_coord = util.first_white_from_left(self.image)

			# If we can't find one, there is no contour in the image
			if first_coord is None:
				self._stroke = ()
				return self._stroke
			
			# Otherwise, get the list of adjacent white coordinates
			self._stroke = self._get_adjacent_whites(first_coord, [])
		return self._stroke
	
	#
	# Represents the edge and inner pixels of a contour, returns a list of coordinates
	#
	def fill(self):
		# Lazy loading
		if self._fill is None:

			# This is where the coordinates will go
			fill = []

			# For each x-value in the contour
			for x in self.xs():

				# Get a list of all of the y-values in the column of the x-value
				xys = [pixel_coordinate[1] for pixel_coordinate in self.stroke() if pixel_coordinate[0] == x]

				# Find the extrema
				min_y = min(xys)
				max_y = max(xys)

				# Add all of the points in-between to fill
				for y in range(min_y, max_y+1):
					fill.append((x, y))
			
			# Turn fill into a tuple for immutability and assign to _fill attribute
			self._fill = tuple(fill)
		return self._fill

	#
	# Returns a sorted list of all x-values in the contour
	#
	def xs(self):
		# Lazy loading
		if self._xs is None:
			self._xs = sorted(tuple(set([pixel_coordinate[0] for pixel_coordinate in self.stroke()])))
		return self._xs
	
	#
	# Returns a sorted list of all y-values in the contour
	#
	def ys(self):
		# Lazy loading
		if self._ys is None:
			self._ys = sorted(tuple(set([pixel_coordinate[1] for pixel_coordinate in self.stroke()])))
		return self._ys