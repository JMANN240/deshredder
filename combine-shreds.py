from PIL import Image

#
# Represents a shred of paper
#

class Shred:
    def __init__(self, image):
        self.image = image
        
        # Generate left sample
        self._left_sample = []
