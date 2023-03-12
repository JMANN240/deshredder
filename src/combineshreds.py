from PIL import Image
import sys

#
# Represents a shred of paper
#

class Shred:
	def __init__(self, image):
		
		# Initialize members
		self.image = image
		# Samples are array of bools. True if "white enough", false otherwise
		self._left_sample = []
		self._right_sample = []
		self._search_depth = 2	# How many pixels should we look into the sample?
		
		# Useful variables
		SATURATION_THRESHOLD = 128 # S value for saturated vs not
		WHITE_THRESHOLD = 192 # How much value for a pixel to be whites?

		# Convert to HSV
		self.image = self.image.convert("HSV")

		# Get left and right samples
		pixel = self.image.load()
		for y in range(self.image.height):

			# Get left sample
			# Look left until we find an unsaturated pixel
			x = 0
			while pixel[x, y][1] > SATURATION_THRESHOLD:
				x += 1
				# Just in case
				if x > self.image.width / 2:
					break
			# Look a few pixels in and check for a blackish one
			for xDepth in range(x, x + self._search_depth):
				if pixel[xDepth, y][2] < WHITE_THRESHOLD:
					self._left_sample.append(True)
					break
			else:
				self._left_sample.append(False)

			# Get right sample
			# Look right until we find an unsaturated pixel
			x = self.image.width - 1
			while pixel[x, y][1] > SATURATION_THRESHOLD:
				x -= 1
				# Just in case
				if x < self.image.width / 2:
					break
			# Look a few pixels in and check for a blackish one
			for xDepth in range(0, self._search_depth):
				if pixel[x - xDepth, y][2] < WHITE_THRESHOLD:
					self._right_sample.append(True)
					break
			else:
				self._right_sample.append(False)
	
	# Returns a boolean indicating of the right side of this shred aligns with
	# the left side of the provided shred. The "closeness" of the match can be
	# supplied with the confidence interval argument
	def aligns_left_of(self, other_shred, confidence_interval):
		matches = 0
		checks = 0

		for i in range(min(len(self._right_sample), len(other_shred._left_sample))):
			left = self._right_sample[i]
			right = other_shred._left_sample[i]
			if left and right:
				matches += 1
				checks += 1
			elif left or right:
				checks += 1
		
		print(matches / checks)
		return (matches / checks) >= confidence_interval

#
# Run tests
#

if __name__ == '__main__':
	if (len(sys.argv) < 2):
		print("To run this file, give a shred number to test")
		exit()

	pickedShredNumber = int(sys.argv[1])
	pickedShred = Shred(Image.open(f"intermediaries/shred_{pickedShredNumber}_example_ideal_saturation.png"))

	for i in range(5):
		comparedShred = Shred(Image.open(f"intermediaries/shred_{i}_example_ideal_saturation.png"))
		if pickedShred.aligns_left_of(comparedShred, 0.5):
			print(f"Shred {pickedShredNumber} goes to the left of shred {i}")
		else:
			print(f"Shred {pickedShredNumber} does not go to the left of shred {i}")
		