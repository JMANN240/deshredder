from PIL import Image
from contour import Contour
import math

#
# Take a subimage and convolve it with the given kernel with respect to saturation
#
def convolve_subimage(subimage, kernel):
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
# Convolve an image by saturation using a kernel
# Generates another image where the pixel values are the values of the convolution of each subimage
#
def convolve_image(image, kernel, checkpoint_name=None):
	image = image.convert('HSV')
	convolution = Image.new('L', (image.width, image.height), color=0)
	(kernel_width, kernel_height) = (len(kernel[0]), len(kernel))
	kernel_edge_width = int((kernel_width-1)/2)
	kernel_edge_height = int((kernel_height-1)/2)
	for x in range(kernel_edge_width, image.width-kernel_edge_width-2):
		for y in range(kernel_edge_height, image.height-kernel_edge_height-2):
			subimage = image.crop((x, y, x+kernel_width, y+kernel_height))
			convolved_value = convolve_subimage(subimage, kernel)
			convolved_value = round(convolved_value*255)
			convolved_value = 255 if convolved_value > 64 else 0
			convolution.putpixel((x, y), convolved_value)
		if checkpoint_name is not None:
			convolution.save(checkpoint_name)
	return convolution

#
# Get all of the shred images in a convolution
#
def get_convolution_contours(convolution, size_threshold=100):
	# A list to hold the contours
	shred_contours = []

	# Until we've found every shred in the image:
	while True:
		# Instantiate a contour object with the current image
		my_contour = Contour(convolution)

		# If we can't find any more edges, we've grabbed every shred
		if len(my_contour.stroke()) == 0:
			break

		# If we've found an edge (that's more than just a small blob), we'll make
		# note of it
		elif len(my_contour.stroke()) >= size_threshold:
			shred_contours.append(my_contour)

		# Fill in the edge we just got with black
		for pixel_coordinate in my_contour.fill():
			convolution.putpixel(pixel_coordinate, 0)
	
	return shred_contours

#
# Figure out how much to rotate the contours
#
def get_contour_rotations(contour, try_thetas):
	best_area = math.inf

	# We'll rotate the shred towards whichever orientation it's closest to
	if math.degrees(contour.theta()) > 45:
		starting_angle = 90-math.degrees(contour.theta())
	else:
		starting_angle = -math.degrees(contour.theta())
	best_theta = starting_angle

	# Try some thetas near the "best" theta
	for try_theta in try_thetas:
		rotated_shred_contour_image = contour.shred_image().rotate(starting_angle+try_theta, expand=True)
		rotated_shred_contour = Contour(rotated_shred_contour_image)
		area = rotated_shred_contour.shred_image().width * rotated_shred_contour.shred_image().height
		if area < best_area:
			best_area = area

	return best_theta

#
# Dialate or erode an image
# For internal use only
#
def _dialate_erode(image, test_color):
	dialated = image.copy()
	(w, h) = dialated.size
	changes = (
		(-1, -1),
		(0, -1),
		(1, -1),
		(-1, 0),
		(1, 0),
		(-1, 1),
		(0, 1),
		(1, 1)
	)
	for x in range(w):
		for y in range(h):
			if image.getpixel((x, y)) == test_color:
				for change in changes:
					try:
						dialated.putpixel((x+change[0], y+change[1]), test_color)
					except:
						pass
	return dialated


#
# Dialate an image
#
def dialate(image):
	return _dialate_erode(image, (255, 255, 255))


#
# Erode an image
#
def erode(image):
	return _dialate_erode(image, (0, 0, 0))

def expand_bounding_box(bounding_box, n):
	return (bounding_box[0]-n, bounding_box[1]-n, bounding_box[2]+n, bounding_box[3]+n)

def offset_bounding_box(bounding_box, x, y):
	return (bounding_box[0]+x, bounding_box[1]+y, bounding_box[2]+x, bounding_box[3]+y)

def first_white_from_left(image):
	(image_width, image_height) = image.size
	for x in range(image_width):
		for y in range(image_height):
			value = image.getpixel((x, y))
			if value == 255:
				return (x, y)
	return None

def last_white_after_first_white_from_left(image):
	(image_width, image_height) = image.size
	found_white_in_image = False
	for x in range(image_width):
		found_white_in_column = False
		for y in range(image_height):
			value = image.getpixel((x, y))
			if value == 255:
				found_white_in_image = True
				found_white_in_column = True
				break
		if not found_white_in_column and found_white_in_image:
			return (x-1, y)
	if found_white_in_column and found_white_in_image:
		return (image_width-1, image_height-1)
	return None

def first_white_from_top(image):
	(image_width, image_height) = image.size
	for y in range(image_height):
		for x in range(image_width):
			value = image.getpixel((x, y))
			if value == 255:
				return (x, y)
	return None

def last_white_after_first_white_from_top(image):
	(image_width, image_height) = image.size
	found_white_in_image = False
	for y in range(image_height):
		found_white_in_row = False
		for x in range(image_width):
			value = image.getpixel((x, y))
			if value == 255:
				found_white_in_image = True
				found_white_in_row = True
		if not found_white_in_row and found_white_in_image:
			return y-1
	if found_white_in_row and found_white_in_image:
		return (image_width-1, image_height-1)
	return None

def extract_and_pass_back(image, box):
	left_crop = image.crop((box[0], 0, box[2]+2, image.height-1))
	right_crop = image.crop((box[2]+1, 0, image.width-1, image.height-1))
	shred_crop = left_crop.crop((0, box[1], left_crop.width-1, box[3]+1))
	return (shred_crop, right_crop)

def get_shred_box(image):
	(image_width, image_height) = image.size
	left = first_white_from_left(image)
	if left is None:
		return None
	right = last_white_after_first_white_from_left(image)
	left_crop = image.crop((left, 0, right+2, image_height-1))
	upper = first_white_from_top(left_crop)
	lower = last_white_after_first_white_from_top(left_crop)
	return (left, upper, right, lower)

def right_white_on_bottom(image):
	last_row_y = image.height-1
	found_white = False
	for x in range(image.width):
		if image.getpixel((x, last_row_y)) == 255:
			found_white = True
		elif found_white:
			return (x-1, last_row_y)
	if found_white:
		return (image.width-1, last_row_y)
	return None

def bottom_white_on_right(image):
	last_col_x = image.width-1
	found_white = False
	for y in range(image.height):
		if image.getpixel((last_col_x, y)) == 255:
			found_white = True
		elif found_white:
			return (last_col_x, y-1)
	if found_white:
		return (last_col_x, image.height-1)
	return None

def first_all_white_from_left(image):
	for x in range(image.width):
		whites = [image.getpixel((x,y)) == 255 for y in range(image.height)]
		if all(whites):
			return x
	return None

def first_all_white_from_right(image):
	for x in range(image.width-1, -1, -1):
		whites = [image.getpixel((x,y)) == 255 for y in range(image.height)]
		if all(whites):
			return x
	return None

def first_all_white_from_top(image):
	for y in range(image.height):
		whites = [image.getpixel((x,y)) == 255 for x in range(image.width)]
		if all(whites):
			return y
	return None

def first_all_white_from_bottom(image):
	for y in range(image.height-1, -1, -1):
		whites = [image.getpixel((x,y)) == 255 for x in range(image.width)]
		if all(whites):
			return y
	return None

def coordinate_in_bounds(image, coordinate):
	return coordinate[0] >= 0 and coordinate[0] < image.width and coordinate[1] >= 0 and coordinate[1] < image.height