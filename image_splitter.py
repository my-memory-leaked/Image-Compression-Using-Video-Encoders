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

def hilbert_curve(n):
    """ Generate Hilbert curve points for a grid of size n x n. """
    def hilbert(x, y, xi, xj, yi, yj, n):
        if n <= 0:
            yield x + (xi + yi) // 2, y + (xj + yj) // 2
        else:
            yield from hilbert(x, y, yi // 2, yj // 2, xi // 2, xj // 2, n - 1)
            yield from hilbert(x + xi // 2, y + xj // 2, xi // 2, xj // 2, yi // 2, yj // 2, n - 1)
            yield from hilbert(x + xi // 2 + yi // 2, y + xj // 2 + yj // 2, xi // 2, xj // 2, yi // 2, yj // 2, n - 1)
            yield from hilbert(x + xi // 2 + yi, y + xj // 2 + yj, -yi // 2, -yj // 2, -xi // 2, -xj // 2, n - 1)
    
    return list(hilbert(0, 0, n, 0, 0, n, int(n).bit_length() - 1))

def slice_image_hilbert(input_image_path, output_folder, tile_size=256):
    output_path = os.path.join(output_folder, 'hilbert')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    image = Image.open(input_image_path)
    image_width, image_height = image.size

    x_tiles = (image_width + tile_size - 1) // tile_size
    y_tiles = (image_height + tile_size - 1) // tile_size

    max_tiles = max(x_tiles, y_tiles)
    curve_order = hilbert_curve(2**(max_tiles.bit_length()))

    tile_number = 0
    for x, y in curve_order:
        if x >= x_tiles or y >= y_tiles:
            continue
        left = x * tile_size
        top = y * tile_size
        right = min(left + tile_size, image_width)
        bottom = min(top + tile_size, image_height)

        if left >= image_width or top >= image_height:
            continue

        tile = image.crop((left, top, right, bottom))
        tile.save(os.path.join(output_path, f"tile_{tile_number}.png"))
        tile_number += 1
        if tile_number >= x_tiles * y_tiles:
            break

    print(f"Sliced image into {tile_number} tiles and saved to '{output_path}' folder.")

# Użycie funkcji:
input_image_path = 'pictures/PIA04230.tif'  # Zastąp 'path_to_your_image.png' ścieżką do swojego obrazu
output_folder = 'output'

# Wyczyszczenie folderu output przed przetwarzaniem
clear_output_folder(output_folder)

# Wywołanie wszystkich funkcji
slice_image(input_image_path, output_folder)  # Wywołanie funkcji dzielącej obraz rząd po rzędzie
slice_image_spiral(input_image_path, output_folder)  # Wywołanie funkcji dzielącej obraz spiralnie
slice_image_hilbert(input_image_path, output_folder)  # Wywołanie funkcji dzielącej obraz krzywą Hilberta
