import logging
import util
from PIL import Image, ImageFilter
import kernels
from time import sleep, time
import math
import sys
import os
import contour
import click
import steps
# from combineshreds import Shred
sys.setrecursionlimit(10000)
logging.basicConfig(level=logging.DEBUG)

# Preprocess commandline args
@click.command()
@click.option("-s", "--start", default=0, help="Which step to begin from")
@click.option("-e", "--end", default=4, help="Which step to end on")
@click.option("-k", "--kernel-size", default=7, help="Size of convolution kernel")
@click.argument("input-file", type=str)
@util.timeit
def deshred(start, end, kernel_size, input_file):
	step = start
	_, input_name = os.path.split(input_file)
	mask_path = f"intermediaries/mask_{input_name}"
	shred_path = lambda index: f"intermediaries/shred_{index}_{input_name}"
	image = Image.open(input_file)
	if step == 0:
		mask = steps.step_1(image)
		mask.save(mask_path)
		sat_val_mask = util.mask_image_saturation_value(image)
		sat_val_mask.save(f"intermediaries/sat_val_mask_{input_name}")
		step += 1
	if step == end:
		return
	mask = Image.open(mask_path)
	if step == 1:
		shreds = steps.step_2(image, mask)
		for index, shred in enumerate(shreds):
			shred.save(shred_path(index))
		step += 1
	if step == end:
		return

if __name__ == '__main__':
	deshred()
