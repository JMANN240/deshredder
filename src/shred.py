from PIL import Image
import sys
import util
import logging
from time import sleep

#
# Represents a shred of paper
#

class Shred:
	def __init__(self, image, samples, search_depth=3, black_threshold=3, max_search_depth=20):
		
		# Initialize members
		self.image = image
		# Samples are array of bools. True if "white enough", false otherwise
		self._samples = samples
		self._left_sample = []
		self._right_sample = []
		self._search_depth = search_depth	# How many pixels should we look into the sample?
		self._black_threshold = black_threshold	# How many of them need to be black for it to be counted as black?
		self._max_search_depth = max_search_depth

		self._calculate_samples()

	def _calculate_samples(self):
		# Reset the samples
		self._left_sample = []
		self._right_sample = []

		# Useful variables
		SATURATION_THRESHOLD = 128 # S value for saturated vs not
		WHITE_THRESHOLD = 192 # How much value for a pixel to be whites?

		# Convert to HSV
		hsv_image = self.image.convert("HSV")

		# Get left and right samples
		pixel = hsv_image.load()
		for y_portion in range(self._samples):
			y = int((hsv_image.height-1) * (y_portion / (self._samples-1)))

			# Get left sample
			# Look left until we find an unsaturated pixel
			x = 0
			while pixel[x, y][1] > SATURATION_THRESHOLD:
				x += 1
				# Just in case
				if x > self._max_search_depth:
					break
			# Look a few pixels in and check for a blackish one
			blacks = 0
			for xDepth in range(self._search_depth):
				if pixel[x+xDepth, y][2] < WHITE_THRESHOLD:
					blacks += 1
			self._left_sample.append(blacks >= self._black_threshold)


			# Get right sample
			# Look right until we find an unsaturated pixel
			x = hsv_image.width - 1
			while pixel[x, y][1] > SATURATION_THRESHOLD:
				x -= 1
				# Just in case
				if x < hsv_image.width-self._max_search_depth:
					break
			# Look a few pixels in and check for a blackish one
			blacks = 0
			for xDepth in range(self._search_depth):
				if pixel[x-xDepth, y][2] < WHITE_THRESHOLD:
					blacks += 1
			self._right_sample.append(blacks >= self._black_threshold)
	
	# Returns a float indicating if the right side of this shred aligns with
	# the left side of the provided shred.
	def aligns_left_of(self, other_shred):
		matches = 0
		checks = 0

		for right, left in zip(self._right_sample, other_shred._left_sample):
			checks += 1
			if left == right:
				matches += 1
		
		if checks == 0:
			return 0

		print(matches, checks)
		confidence = matches / checks
		logging.debug(f"Confidence: {round(confidence, 2)}")
		return confidence
	
	# Like 'aligns_left_of' but reverse
	def aligns_right_of(self, other_shred):
		return other_shred.aligns_left_of(self)

	def attach_left_of(self, other_shred):
		# Although the images can be different widths, their height must
		# be identical. Just in case it isn't we'll truncate the taller one
		min_height = min(self.image.height, other_shred.image.height)
		self.image.resize((self.image.width, min_height))
		other_shred.image.resize((other_shred.image.width, min_height))

		# Create a new image to hold the combined images
		combined_image = Image.new("RGB", (self.image.width + other_shred.image.width, self.image.height), "white")

		combined_image.paste(self.image, (0, 0))
		combined_image.paste(other_shred.image, (self.image.width, 0))

		# Save this as the new image for this object
		new_shred = Shred(combined_image, self._samples)
		return new_shred

	def attach_right_of(self, other_shred):
		return other_shred.attach_left_of(self)