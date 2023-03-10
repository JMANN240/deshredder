# Paper Deshredder
## Reconstructing shredded documents using computer-vision

## How it works

Paper Deshredder is a python prorgram that takes a picture of paper shreds as input and gives you a reconstructed document as an image. Paper Deshredder uses computer vision and image processing to identify the shreds in the image, re-orient them, and stitch them back together in to correct order.

## Steps
1) Run a saturation convolution on the input image do detect shred boundaries
2) Identify each shred using the convolution image, extract the shreds, and re-orient the shreds
3) Analyze each shred and stitch the reconstructed image

## Constraints
- The input must be a single image containing all shreds to be considered
- The shreds must be placed on a saturated surface (distinctly not black or white)
- The shreds must have relatively straight edges and be rectangular in shape
- The shreds should be "fairly upright", such that the angle between the bottom of the shred and the bottom of the picture is less than 45 degrees
- The content of documents to deshred must be grayscale in color

## Freedoms
- Shreds can be placed in any orientation except for previously defined constraints

## Running
- To execute this program, run main.py with the --help option to list arguments and options.

## NOTE: YOU MUST BE IN THE ROOT DIRECTORY WHEN YOU RUN `python src/main.py`