from PIL import Image

kernel_size = (9, 9)

h_lines = [
	[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
	[1,1,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1,1],
	[0,0,0,0,0,0,0,0,0],
	[-1,-1,-1,-1,-1,-1,-1,-1,-1],
	[-1,-1,-1,-1,-1,-1,-1,-1,-1],
	[-1,-1,-1,-1,-1,-1,-1,-1,-1],
	[-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5]
]

d_lines = [
	[1,1,1,1,1,1,1,1,0],
	[1,1,1,1,1,1,1,0,-1],
	[1,1,1,1,1,1,0,-1,-1],
	[1,1,1,1,1,0,-1,-1,-1],
	[1,1,1,1,0,-1,-1,-1,-1],
	[1,1,1,0,-1,-1,-1,-1,-1],
	[1,1,0,-1,-1,-1,-1,-1,-1],
	[1,0,-1,-1,-1,-1,-1,-1,-1],
	[0,-1,-1,-1,-1,-1,-1,-1,-1],
]

donut = [
	[1,0,0,0,0,0,0,0,1],
	[0,1,0,0,0,0,0,1,0],
	[0,0,1,0,0,0,1,0,0],
	[0,0,0,1,0,1,0,0,0],
	[0,0,0,0,1,0,0,0,0],
	[0,0,0,1,0,1,0,0,0],
	[0,0,1,0,0,0,1,0,0],
	[0,1,0,0,0,0,0,1,0],
	[1,0,0,0,0,0,0,0,1],
]

kernel = d_lines

def convolve(subimage):
	value = 0
	test_pixel = subimage.getpixel(((kernel_size[0]-1)/2, (kernel_size[1]-1)/2))
	for x in range(kernel_size[0]):
		for y in range(kernel_size[1]):
			current_pixel = subimage.getpixel((x, y))
			value += (sum([abs(test_pixel[i]-current_pixel[i]) for i in range(3)]) / 3) * kernel[y][x]
	value /= sum([sum([abs(element) for element in row]) for row in kernel])
	value = round(value)
	value = value > 8
	value *= 255
	return (value, value, value)

def dialate_erode(image, test_color):
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

def dialate(image):
	return dialate_erode(image, (255, 255, 255))

def erode(image):
	return dialate_erode(image, (0, 0, 0))

with Image.open('example2.png') as img:
	img = img.resize((round(512*img.size[0]/img.size[1]), 512))
	(w, h) = img.size
	convolution = Image.new('RGB', (w-(kernel_size[0]-1), h-(kernel_size[1]-1)))
	for x in range(w-(kernel_size[0]-1)):
		for y in range(h-(kernel_size[1]-1)):
			convolution.putpixel((x, y), convolve(img.crop((x, y, x+(kernel_size[0]), y+(kernel_size[1])))))
		print(round(x/(w-(kernel_size[0]-1)), 2))
		convolution.save('convolution.png')
	#convolution = erode(convolution)
	#convolution = erode(convolution)
	#convolution = dialate(convolution)
	#convolution = dialate(convolution)
	convolution.save('convolution.png')
