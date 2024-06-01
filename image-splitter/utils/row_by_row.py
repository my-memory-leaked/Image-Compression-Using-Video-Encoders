import os
from PIL import Image

def slice_image_row_by_row(input_image_path, output_folder, tile_size=256):
    output_path = os.path.join(output_folder, 'row_by_row')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    image = Image.open(input_image_path)
    image_width, image_height = image.size
    
    tile_number = 0
    for top in range(0, image_height, tile_size):
        for left in range(0, image_width, tile_size):
            bottom = min(top + tile_size, image_height)
            right = min(left + tile_size, image_width)
            
            tile = image.crop((left, top, right, bottom))
            tile.save(os.path.join(output_path, f"tile_{tile_number}.png"))
            tile_number += 1

    print(f"Sliced image into {tile_number} tiles and saved to '{output_path}' folder.")
