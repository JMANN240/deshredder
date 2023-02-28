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

def first_white_from_left(image):
	(image_width, image_height) = image.size
	for x in range(image_width):
		for y in range(image_height):
			value = image.getpixel((x, y))
			if value == 255:
				return x
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
			return x-1
	if found_white_in_column and found_white_in_image:
		return image_width-1
	return None

def first_white_from_top(image):
	(image_width, image_height) = image.size
	for y in range(image_height):
		for x in range(image_width):
			value = image.getpixel((x, y))
			if value == 255:
				return y
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
		return image_height-1
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
