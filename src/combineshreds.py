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
		self._search_depth = 3	# How many pixels should we look into the sample?

		# Convert to HSV
		self.image = self.image.convert("HSV")

		# Get left and right samples
		pixel = self.image.load()
		for y in range(self.image.height):

			# Get left sample
			# Look left until we find an unsaturated pixel
			x = 0
			while pixel[x, y][1] > 128:
				x += 1
				# Just in case
				if x > self.image.width / 2:
					break
			# Look a few pixels in and check for a blackish one
			for xDepth in range(x, x + self._search_depth):
				if pixel[xDepth, y][2] > 128:
					self._left_sample.append(True)
					break
			else:
				self._left_sample.append(False)
		
		print(self._left_sample)

shred = Shred(Image.open("intermediaries/shred_1_example_ideal_saturation.png"))
		