import os
from PIL import Image

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
