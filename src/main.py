import logging
import util
from PIL import Image, ImageFilter
import kernels
from time import sleep, time
import math
import sys
import os
import contour
import steps
sys.setrecursionlimit(10000)

logging.basicConfig(level=logging.DEBUG)

with Image.open('examples/example_ideal_saturation.png') as image:
    logging.info("Starting Step 1")
    convolution = steps.step_1(image, kernel_size=7)
    logging.info("Step 1 Complete")
    convolution.show()
    logging.info("Starting Step 2")
    shred_images = steps.step_2(image, convolution)
    logging.info("Step 2 Complete")
    for index, shred_image in enumerate(shred_images):
        Image.save(f"intermediaries/shred_{index}.png")