import os
import sys

# Add the path to the utils module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

from utils.helper import clear_output_folder
from utils.row_by_row import slice_image_row_by_row
from utils.spiral import slice_image_spiral
from utils.hilbert import slice_image_hilbert
from utils.column_by_column import slice_image_column_by_column  # New import

def run_image_splitter(input_image_path, output_folder):
    # Check if the image file exists
    if not os.path.exists(input_image_path):
        print(f"File not found: {input_image_path}")
        return

    # Clear the output folder before processing
    clear_output_folder(output_folder)

    # Display the size of the original image
    original_size = os.path.getsize(input_image_path)
    print(f"Original image size: {original_size} bytes")

    # Call all slicing functions
    slice_image_row_by_row(input_image_path, output_folder)
    slice_image_spiral(input_image_path, output_folder)
    slice_image_hilbert(input_image_path, output_folder)
    slice_image_column_by_column(input_image_path, output_folder)  # New call

    # Display the size of the split tiles
    total_tile_size = get_total_tile_size(output_folder)
    print(f"Total size of all tiles: {total_tile_size} bytes")

def get_total_tile_size(output_folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(output_folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size

if __name__ == "__main__":
    # No default values
    print("This script is intended to be imported and called from another script.")
