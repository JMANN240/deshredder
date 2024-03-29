import kernels
import util
from contour import Contour
import logging

#
# Take in an image, return its saturation convolution
#
@util.timeit
def step_1(image):
    masked_image = util.mask_image(image)
    logging.debug("Masked image")
    return masked_image

#
# Take an image and its convolution and return the shred images
#
@util.timeit
def step_2(image, convolution):
    contours = util.get_convolution_contours(convolution)
    logging.debug("Got contours")
    for i, contour in enumerate(contours):
        contour.contour_image().save(f"intermediaries/contour_{i}.png")
    shreds = [image.crop(contour.bounding_box()) for contour in contours]
    logging.debug("Got shreds")
    for i, shred in enumerate(shreds):
        shred.save(f"intermediaries/shred_{i}.png")
    contour_rotations = [util.get_contour_rotations(contour, []) for contour in contours]
    logging.debug("Got contour rotations")
    rotated_shreds = [shred.rotate(contour_rotation, fillcolor=(255,0,0), expand=True) for shred, contour_rotation in zip(shreds, contour_rotations)]
    logging.debug("Rotated shreds")
    rotated_convolution_shreds = [contour.shred_image().rotate(contour_rotation, expand=True) for contour, contour_rotation in zip(contours, contour_rotations)]
    logging.debug("Rotated convolution shreds")
    rotated_convolution_shred_contours = [Contour(rotated_convolution_shred) for rotated_convolution_shred in rotated_convolution_shreds]
    logging.debug("Created rotated shred contours")
    cropped_rotated_shreds = [rotated_shred.crop(rotated_convolution.bounding_box()) for rotated_shred, rotated_convolution in zip(rotated_shreds, rotated_convolution_shred_contours)]
    logging.debug("Cropped rotated shreds")
    return cropped_rotated_shreds