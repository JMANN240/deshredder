import logging
import util
from PIL import Image
import kernels
from time import sleep, time
import math
import sys
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
# Convolve and image using a kernel
# Generates another image where the pixel values are the values of the convolution of each subimage
#
def convolve_image(image, kernel, checkpoint_name=None):
	(kernel_width, kernel_height) = (len(kernel[0]), len(kernel))
	(image_width, image_height) = image.size
	total_pixels = image_width * image_height
	convolution = Image.new('L', (image_width-(kernel_width-1), image_height-(kernel_height-1)))
	(convolution_width, convolution_height) = convolution.size
	for x in range(convolution_width):
		for y in range(convolution_height):
			subimage = image.crop((x, y, x+kernel_width, y+kernel_height))
			convolved_value = convolve_subimage(subimage, kernel)
			convolved_value = round(convolved_value*255)
			convolved_value = 255 if convolved_value > 16 else 0
			convolution.putpixel((x, y), convolved_value)
			logging.info(f"{round(100*(x*image_height+y+1)/total_pixels, 2)}%")
		if checkpoint_name is not None:
			convolution.save(checkpoint_name)
	return convolution

with Image.open('convolution.png') as convolution:
	# img = img.convert('L')
	# convolution = convolve_image(img, kernels.basic(3), 'convolution.png')
	# # convolution = convolve_image(convolution, kernels.basic(5,5), 'convolution.png')
	# sleep(1)
	# convolution.save('convolution.png')

	my_contour = contour.Contour(convolution)

	island = Image.new('L', (convolution.width, convolution.height))
	for pixel_coordinate in my_contour.whites:
		island.putpixel(pixel_coordinate, 255)
	island.show()