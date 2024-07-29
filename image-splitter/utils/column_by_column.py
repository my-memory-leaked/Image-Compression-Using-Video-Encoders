import os
from PIL import Image

def slice_image_column_by_column(input_image_path, output_folder, tile_size=256):
    output_path = os.path.join(output_folder, 'column_by_column')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    image = Image.open(input_image_path)
    image_width, image_height = image.size
    
    tile_number = 0
    for left in range(0, image_width, tile_size):
        for top in range(0, image_height, tile_size):
            right = min(left + tile_size, image_width)
            bottom = min(top + tile_size, image_height)
            
            tile = image.crop((left, top, right, bottom))
            tile.save(os.path.join(output_path, f"tile_{tile_number}.png"))
            tile_number += 1

    print(f"Sliced image into {tile_number} tiles and saved to '{output_path}' folder.")
