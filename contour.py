import util
from PIL import Image
import math

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
		self._contour_image = None

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

			# If it satisfies these conditions, check to see if it is white
			if new_pixel and pixel_in_image:
				pixel_is_white = self.image.getpixel(neighbor_coordinate) == 255 # White?
				if pixel_is_white:
					self._get_adjacent_whites(neighbor_coordinate, list)

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
	
	#
	# Returns an image representing the contour
	#
	def contour_image(self):
		if self._contour_image is None:
			self._contour_image = Image.new('L', (self.image.width, self.image.height))
			for pixel_coordinate in self.stroke():
				self._contour_image.putpixel(pixel_coordinate, 255)
		return self._contour_image
	
	#
	# Return a cropped image representing the unrotated shred
	#
	def shred_image(self):
		return self.contour_image().crop(self.bounding_box())
		
	
	#
	# Returns a bounding-box for the countour as (left, upper, right, lower)
	#
	def bounding_box(self):
		left = self.first_white_from_left()[0]
		upper = self.first_white_from_top()[1]
		right = self.first_white_from_right()[0]+1
		lower = self.first_white_from_bottom()[1]+1
		return (left, upper, right, lower)

	#
	# Returns the coordinate of the first uppermost white pixel from the left
	#
	def first_white_from_left(self):
		contour_image = self.contour_image()
		for x in range(contour_image.width):
			for y in range(contour_image.height):
				value = contour_image.getpixel((x, y))
				if value == 255:
					return (x, y)
		return None

	#
	# Returns the coordinate of the first lowermost white pixel from the right
	#
	def first_white_from_right(self):
		contour_image = self.contour_image()
		for x in range(contour_image.width-1, -1, -1):
			for y in range(contour_image.height-1, -1, -1):
				value = contour_image.getpixel((x, y))
				if value == 255:
					return (x, y)
		return None

	#
	# Returns the coordinate of the first leftmost white pixel from the top
	#
	def first_white_from_top(self):
		contour_image = self.contour_image()
		for y in range(contour_image.height):
			for x in range(contour_image.width):
				value = contour_image.getpixel((x, y))
				if value == 255:
					return (x, y)
		return None

	#
	# Returns the coordinate of the first rightmost white pixel from the bottom
	#
	def first_white_from_bottom(self):
		contour_image = self.contour_image()
		for y in range(contour_image.height-1, -1, -1):
			for x in range(contour_image.width-1, -1, -1):
				value = contour_image.getpixel((x, y))
				if value == 255:
					return (x, y)
		return None

	#
	# Returns the angle theta between the bottom edge and the bottom-right side of the shred
	#
	def theta(self):
		# Get the points of the angle
		bottom = self.first_white_from_bottom()
		right = self.first_white_from_right()

		# Find the leg lengths
		dx = right[0]-bottom[0]
		dy = bottom[1]-right[1] # Flip the order because of weird coordinate stuff

		# Use atan2 to find the angle in radians
		return math.atan2(dy, dx)