import os
import numpy as np
import cv2

class MyImage:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        if self.image is None:
            raise ValueError(f"Image at path {image_path} could not be loaded.")
        self.height, self.width, self.channels = self.image.shape

    def split_image(self, grid_size, transform=None):
        # Calculate the number of tiles in both dimensions
        num_tiles_y = int(np.ceil(self.height / grid_size))
        num_tiles_x = int(np.ceil(self.width / grid_size))
        
        # Initialize a list to hold all the tiles
        tiles = []
        
        # Iterate over the grid to create the tiles
        for y in range(num_tiles_y):
            for x in range(num_tiles_x):
                # Calculate the start and end points for each tile
                start_y = y * grid_size
                end_y = min(start_y + grid_size, self.height)
                start_x = x * grid_size
                end_x = min(start_x + grid_size, self.width)
                
                # Extract the tile
                tile = self.image[start_y:end_y, start_x:end_x]
                
                # Apply the transformation if one is provided
                if transform:
                    tile = transform(tile)
                    
                # Add the tile to the list
                tiles.append(tile)
        
        return tiles

    def save_tiles(self, tiles, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for i, tile in enumerate(tiles):
            tile_path = os.path.join(output_dir, f"tile_{i:04d}.png")
            tile_bgr = cv2.cvtColor(tile, cv2.COLOR_RGB2BGR)
            cv2.imwrite(tile_path, tile_bgr)
