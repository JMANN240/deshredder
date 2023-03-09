from PIL import Image

#
# Represents a shred of paper
#

class Shred:
    def __init__(self, image):
        self.image = image
        pixelGrid = image.load()

        # Generate side samples
        self._left_sample = []
        self._right_sample = []

        # For every pixel along the side of the image, move towards the center
        # until we find a black or white pixel
        for y in range(image.height):
            
            # Left sample
            x = 0
            while (pixelGrid[x, y] == None):
                x += 1
            _left_sample.append(pixelGrid[x, y])

            # Right sample
            x = image.width - 1
            while (pixelGrid[x, y] == None):
                x -= 1
            right_sample.append(pixelGrid[x,y])

    #def __convolve_sample(sample):   