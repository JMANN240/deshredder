import util

def get_adjacent_whites(image, x, y, list, depth=0):
	current_value = image.getpixel((x,y))
	if (current_value == 255): # If the current pixel is white
		list.append((x,y))
	neighbor_coordinates = ((x-1, y), (x, y-1), (x+1, y), (x, y+1))
	for neighbor_coordinate in neighbor_coordinates:
		if neighbor_coordinate not in list and util.coordinate_in_bounds(image, neighbor_coordinate) and image.getpixel(neighbor_coordinate) == 255:
			get_adjacent_whites(image, neighbor_coordinate[0], neighbor_coordinate[1], list, depth+1)
	return list

#
# Represents a closed-loop of white pixels
#
class Contour:
	def __init__(self, image):
		self.image = image
		self._stroke = None
		self._fill = None
		self._xs = None
		self._ys = None
	
	def stroke(self):
		if self._stroke is None:
			first_coord = util.first_white_from_left(self.image)
			if first_coord is None:
				self._stroke = ()
				return self._stroke
			(first_x, first_y) = first_coord
			self._stroke = get_adjacent_whites(self.image, first_x, first_y, [])
		return self._stroke
		
	def fill(self):
		if self._fill is None:
			fill = []
			for x in self.xs():
				xys = [pixel_coordinate[1] for pixel_coordinate in self.stroke() if pixel_coordinate[0] == x]
				min_y = min(xys)
				max_y = max(xys)
				for y in range(min_y, max_y+1):
					fill.append((x, y))
			self._fill = tuple(fill)
		return self._fill

	def xs(self):
		if self._xs is None:
			self._xs = sorted(tuple(set([pixel_coordinate[0] for pixel_coordinate in self.stroke()])))
		return self._xs
	
	def ys(self):
		if self._ys is None:
			self._ys = sorted(tuple(set([pixel_coordinate[1] for pixel_coordinate in self.stroke()])))
		return self._ys