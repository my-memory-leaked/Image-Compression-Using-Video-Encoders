from PIL import Image as PILImage
import numpy as np

class MyImage:
    def __init__(self, path):
        self.path = path
    
    def open(self):
        return PILImage.open(self.path).convert("RGB")
    
    def show(self):
        image = self.open()
        image.show()

    def split_image(self, grid_size):
        image = self.open()
        image = np.array(image)
        h, w, _ = image.shape
        tiles = [image[x:x+grid_size, y:y+grid_size] for x in range(0, h, grid_size) for y in range(0, w, grid_size)]
        return tiles
