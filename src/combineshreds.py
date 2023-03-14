from PIL import Image
import sys
import util
from time import sleep

#
# Represents a shred of paper
#

class Shred:
	def __init__(self, image):
		
		# Initialize members
		self.image = image
		# Samples are array of bools. True if "white enough", false otherwise
		self._samples = 800
		self._left_sample = []
		self._right_sample = []
		self._search_depth = 3	# How many pixels should we look into the sample?
		self._black_threshold = 3	# How many of them need to be black for it to be counted as black?

		self._calculate_samples()

	def _calculate_samples(self):
		# Reset the samples
		self._left_sample = []
		self._right_sample = []

		# Useful variables
		SATURATION_THRESHOLD = 128 # S value for saturated vs not
		WHITE_THRESHOLD = 192 # How much value for a pixel to be whites?

		# Convert to HSV
		self.image = self.image.convert("HSV")

		# Get left and right samples
		pixel = self.image.load()
		for y_portion in range(self._samples):
			y = int((self.image.height-1) * (y_portion / (self._samples-1)))

			# Get left sample
			# Look left until we find an unsaturated pixel
			x = 0
			while pixel[x, y][1] > SATURATION_THRESHOLD:
				x += 1
				# Just in case
				if x > self.image.width / 2:
					break
			# Look a few pixels in and check for a blackish one
			blacks = 0
			for xDepth in range(self._search_depth):
				if pixel[x+xDepth, y][2] < WHITE_THRESHOLD:
					blacks += 1
			self._left_sample.append(blacks >= self._black_threshold)
				

			# Get right sample
			# Look right until we find an unsaturated pixel
			x = self.image.width - 1
			while pixel[x, y][1] > SATURATION_THRESHOLD:
				x -= 1
				# Just in case
				if x < self.image.width / 2:
					break
			# Look a few pixels in and check for a blackish one
			blacks = 0
			for xDepth in range(self._search_depth):
				if pixel[x-xDepth, y][2] < WHITE_THRESHOLD:
					blacks += 1
			self._right_sample.append(blacks >= self._black_threshold)

		# Convert back to RGB
		self.image = self.image.convert("RGB")
	
	# Returns a boolean indicating of the right side of this shred aligns with
	# the left side of the provided shred. The "closeness" of the match can be
	def aligns_left_of(self, other_shred):
		matches = 0
		checks = 0

		for right, left in zip(self._right_sample, other_shred._left_sample):
			if left or right:
				checks += 1
				if left and right:
					matches += 1

		print(f"Confidence: {round(matches / checks, 2)}")
		return (matches / checks)

	def attach_left_of(self, other_shred):
		# Although the images can be different widths, their height must
		# be identical. Just in case it isn't we'll truncate the taller one
		if self.image.height > other_shred.image.height:
			self.image.resize((self.image.width, other_shred.image.height))
		elif other_shred.image.height > self.image.height:
			other_shred.image.resize((other_shred.image.width, self.image.height))

		# Create a new image to hold the combined images
		combined_image = Image.new("RGB", (self.image.width + other_shred.image.width, self.image.height), "white")

		combined_image.paste(self.image, (0, 0))
		combined_image.paste(other_shred.image, (self.image.width, 0))

		# Save this as the new image for this object
		self.image = combined_image
		self._calculate_samples()

#
# Run tests
#

def find_match(shreds):
	for i, left_shred in enumerate(shreds):
		best_match_confidence = 0
		best_match_index = None
		for j, right_shred in enumerate(shreds):
			if i == j:
				continue
			print(f"Comparing shreds {i} and {j}")
			confidence = left_shred.aligns_left_of(right_shred)
			if confidence > best_match_confidence:
				best_match_index = j
				best_match_confidence = confidence
		if best_match_index is None:
			return False
		left_shred.attach_left_of(shreds[best_match_index])
		shreds.remove(shreds[best_match_index])
		return True
	return False

if __name__ == '__main__':

	# Get all shreds (adjust as necessary)
	shreds = []
	for i in range(8):
		shreds.append(Shred(Image.open(f"intermediaries/shred_{i}_example_8_shreds.png")))

	lookingForMatches = True
	while lookingForMatches:
		lookingForMatches = find_match(shreds)

	for index, shred in enumerate(shreds):
		shred.image.save(f"outputs/document{index}.png")