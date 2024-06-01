import os
from PIL import Image

def slice_image_spiral(input_image_path, output_folder, tile_size=256):
    output_path = os.path.join(output_folder, 'spiral')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    image = Image.open(input_image_path)
    image_width, image_height = image.size
    
    x_tiles = (image_width + tile_size - 1) // tile_size
    y_tiles = (image_height + tile_size - 1) // tile_size

    spiral_order = []

    def spiral_coordinates(width, height):
        x_min, x_max = 0, width - 1
        y_min, y_max = 0, height - 1
        while x_min <= x_max and y_min <= y_max:
            for x in range(x_min, x_max + 1):
                spiral_order.append((x, y_min))
            y_min += 1
            for y in range(y_min, y_max + 1):
                spiral_order.append((x_max, y))
            x_max -= 1
            if y_min <= y_max:
                for x in range(x_max, x_min - 1, -1):
                    spiral_order.append((x, y_max))
                y_max -= 1
            if x_min <= x_max:
                for y in range(y_max, y_min - 1, -1):
                    spiral_order.append((x_min, y))
                x_min += 1

    spiral_coordinates(x_tiles, y_tiles)

    tile_number = 0
    for x, y in spiral_order:
        left = x * tile_size
        top = y * tile_size
        right = min(left + tile_size, image_width)
        bottom = min(top + tile_size, image_height)

        if left >= image_width or top >= image_height:
            continue

        tile = image.crop((left, top, right, bottom))
        tile.save(os.path.join(output_path, f"tile_{tile_number}.png"))
        tile_number += 1

    print(f"Sliced image into {tile_number} tiles and saved to '{output_path}' folder.")
