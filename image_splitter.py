import os
import shutil
from PIL import Image

def clear_output_folder(output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

def slice_image(input_image_path, output_folder, tile_size=256):
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

# Użycie funkcji:
input_image_path = 'pictures/PIA04230.tif'  # Zastąp 'path_to_your_image.png' ścieżką do swojego obrazu
output_folder = 'output'

# Wyczyszczenie folderu output przed przetwarzaniem
clear_output_folder(output_folder)

# Wywołanie obu funkcji
slice_image(input_image_path, output_folder)  # Wywołanie funkcji dzielącej obraz rząd po rzędzie
slice_image_spiral(input_image_path, output_folder)  # Wywołanie funkcji dzielącej obraz spiralnie
