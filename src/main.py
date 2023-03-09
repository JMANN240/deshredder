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

#
# Take a subimage and convolve it with the given kernel
#
def convolve_subimage(subimage, kernel):
	(kernel_width, kernel_height) = (len(kernel[0]), len(kernel))
	value = 0
	test_pixel = subimage.getpixel(((kernel_width-1)/2, (kernel_height-1)/2)) / 255
	logging.debug(f"{test_pixel=}")
	for x in range(kernel_width):
		for y in range(kernel_height):
			current_pixel = subimage.getpixel((x, y)) / 255
			value += abs(test_pixel-current_pixel) * kernel[y][x]
	kernel_sum_positive = sum([sum([v for v in row if v > 0]) for row in kernel])
	kernel_sum_negative = sum([sum([v for v in row if v < 0]) for row in kernel])
	kernel_sum_max = max(kernel_sum_positive, kernel_sum_negative)
	return value / kernel_sum_max


#
# Take a subimage and convolve it with the given kernel with respect to saturation
#
def convolve_subimage_saturation(subimage, kernel):
	(kernel_width, kernel_height) = (len(kernel[0]), len(kernel))
	value = 0
	test_pixel = subimage.getpixel(((kernel_width-1)/2, (kernel_height-1)/2))[1] / 255
	for x in range(kernel_width):
		for y in range(kernel_height):
			current_pixel = subimage.getpixel((x, y))[1] / 255
			value += abs(test_pixel-current_pixel) * kernel[y][x]
	kernel_sum_positive = sum([sum([v for v in row if v > 0]) for row in kernel])
	kernel_sum_negative = sum([sum([v for v in row if v < 0]) for row in kernel])
	kernel_sum_max = max(kernel_sum_positive, kernel_sum_negative)
	return value / kernel_sum_max


#
# Convolve an image by value using a kernel
# Generates another image where the pixel values are the values of the convolution of each subimage
#
def convolve_image_value(image, kernel, checkpoint_name=None):
	image = image.convert('L')
	convolution = Image.new('L', (image.width, image.height), color=0)
	(kernel_width, kernel_height) = (len(kernel[0]), len(kernel))
	kernel_edge_width = int((kernel_width-1)/2)
	kernel_edge_height = int((kernel_height-1)/2)
	for x in range(kernel_edge_width, image.width-kernel_edge_width-1):
		for y in range(kernel_edge_height, image.height-kernel_edge_height-1):
			subimage = image.crop((x, y, x+kernel_width, y+kernel_height))
			convolved_value = convolve_subimage(subimage, kernel)
			convolved_value = round(convolved_value*255)
			convolved_value = 255 if convolved_value > 16 else 0
			convolution.putpixel((x, y), convolved_value)
		if checkpoint_name is not None:
			convolution.save(checkpoint_name)
	return convolution


#
# Convolve an image by saturation using a kernel
# Generates another image where the pixel values are the values of the convolution of each subimage
#
def convolve_image_saturation(image, kernel, checkpoint_name=None):
	image = image.convert('HSV')
	convolution = Image.new('L', (image.width, image.height), color=0)
	(kernel_width, kernel_height) = (len(kernel[0]), len(kernel))
	kernel_edge_width = int((kernel_width-1)/2)
	kernel_edge_height = int((kernel_height-1)/2)
	for x in range(kernel_edge_width, image.width-kernel_edge_width-2):
		for y in range(kernel_edge_height, image.height-kernel_edge_height-2):
			subimage = image.crop((x, y, x+kernel_width, y+kernel_height))
			convolved_value = convolve_subimage_saturation(subimage, kernel)
			convolved_value = round(convolved_value*255)
			convolved_value = 255 if convolved_value > 64 else 0
			convolution.putpixel((x, y), convolved_value)
		if checkpoint_name is not None:
			convolution.save(checkpoint_name)
	return convolution

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
		convolution = convolve_image_saturation(img, kernels.basic(7), 'convolution.png')
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
