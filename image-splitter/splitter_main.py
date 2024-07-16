import os
import sys

# Dodanie ścieżki do modułu utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

from utils.helper import clear_output_folder
from utils.row_by_row import slice_image_row_by_row
from utils.spiral import slice_image_spiral
from utils.hilbert import slice_image_hilbert

def run_image_splitter(input_image_path, output_folder):
    # Sprawdzenie, czy plik obrazu istnieje
    if not os.path.exists(input_image_path):
        print(f"File not found: {input_image_path}")
        return

    # Wyczyszczenie folderu output przed przetwarzaniem
    clear_output_folder(output_folder)

    # Wyświetlanie rozmiaru oryginalnego obrazu
    original_size = os.path.getsize(input_image_path)
    print(f"Original {input_image_path} size: {original_size} bytes")

    # Wywołanie wszystkich funkcji
    slice_image_row_by_row(input_image_path, output_folder)
    slice_image_spiral(input_image_path, output_folder)
    slice_image_hilbert(input_image_path, output_folder)

    # Wyświetlanie rozmiaru podzielonych kafelków
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
    # Brak domyślnych wartości
    print("This script is intended to be imported and called from another script.")
