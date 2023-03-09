from PIL import Image

#
# Represents a shred of paper
#

class Shred:
    def __init__(self, image):
        self.image = image

        # Load a pixel grid to make pixel access more efficient
        pixelGrid = image.load()

        # Generate side samples
        self._left_sample = []
        self._right_sample = []
         