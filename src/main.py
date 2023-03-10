import logging
import util
from PIL import Image, ImageFilter
import kernels
from time import sleep, time
import math
import sys
import os
import contour
sys.setrecursionlimit(10000)

# Preprocess commandline args
# Expected input: one optional argument, which is a list of case-insensitive switches
reuseIntermediaries = False

if len(sys.argv) == 2:
	switches = sys.argv[1][1:].lower()

	for switch in switches:
		match switch:
			case 'r':
				reuseIntermediaries = True

# Take an input image with all shreds to be computed, and create an edge map with convolution
# This convolution is reusable, to save time
if not reuseIntermediaries or not os.path.isfile('../input/example_ideal_saturation.png'):
	with Image.open('../input/example_ideal_saturation.png') as img:
		convolution = util.convolve_image(img, kernels.basic(7), 'convolution.png')
		convolution.save('../intermediary/convolution.png')

# A list to hold all the shreds we find
shred_contours = []

# Open the convolution image
with Image.open('../intermediary/convolution.png') as convolution:

	# Until we've found every shred in the image:
	while True:
		# Instantiate a contour object with the current image
		my_contour = contour.Contour(convolution)

		# If we can't find any more edges, we've grabbed every shred
		if len(my_contour.stroke()) == 0:
			break

		# If we've found an edge (that's more than just a small blob), we'll make
		# note of it
		elif len(my_contour.stroke()) >= 100:
			shred_contours.append(my_contour)

		# Fill in the edge we just got with black
		for pixel_coordinate in my_contour.fill():
			convolution.putpixel(pixel_coordinate, 0)

# A list to hold the corrected shreds
rotated_shred_contour_images = []

# For every shred
for shred_index, shred_contour in enumerate(shred_contours):
	print(f"Processing shred {shred_index}")

	best_rotated_shred_contour_image = None
	best_rotated_shred_contour_area = math.inf

	# We'll rotate the shred towards whichever orientation it's closest to
	if math.degrees(shred_contour.theta()) > 45:
		starting_angle = 90-math.degrees(shred_contour.theta())
	else:
		starting_angle = -math.degrees(shred_contour.theta())

	# I have no idea what's happening here
	for epsilon in range(-10,10):
		epsilon /= 2
		rotated_shred_contour_image = shred_contour.shred_image().rotate(starting_angle+epsilon, expand=True)
		rotated_shred_contour = contour.Contour(rotated_shred_contour_image)
		area = rotated_shred_contour.shred_image().width * rotated_shred_contour.shred_image().height
		if area < best_rotated_shred_contour_area:
			best_rotated_shred_contour_area = area
			best_rotated_shred_contour_image = rotated_shred_contour_image
	rotated_shred_contour_images.append(best_rotated_shred_contour_image)

# For every corrected shred
for index, rotated_shred_contour_image in enumerate(rotated_shred_contour_images):
	rotated_shred_contour = contour.Contour(rotated_shred_contour_image.filter(ImageFilter.MaxFilter(3)))
	rotated_shred_contour.shred_image().save(f"../output/shred{index}.png")
	index += 1
