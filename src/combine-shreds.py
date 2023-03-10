from PIL import Image

#
# Represents a shred of paper
#

class Shred:
	def __init__(self, image):
		
		# Initialize members
		self.image = image
		self._left_sample = []
		self._right_sample = []
		self._search_depth = 2	# How many pixels should we look into the sample?

		# Convert to HSV
		self.image = self.image.convert("HSV")

		# Get left and right samples
		pixel = image.load()
		for y in range(image.height):

			# Get left sample
			# Look left until we find an unsaturated pixel
			x = 0
			while pixel[x, y][1] != 0:
				x += 1
			# Look a few pixels in and check if it's black or white
			x += self._search_depth
			self._left_sample.append(pixel[x, y][2] > 127)
			print(self._left_sample)
		