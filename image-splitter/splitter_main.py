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

    # Wywołanie wszystkich funkcji
    slice_image_row_by_row(input_image_path, output_folder)  # Wywołanie funkcji dzielącej obraz rząd po rzędzie
    slice_image_spiral(input_image_path, output_folder)  # Wywołanie funkcji dzielącej obraz spiralnie
    slice_image_hilbert(input_image_path, output_folder)  # Wywołanie funkcji dzielącej obraz krzywą Hilberta

if __name__ == "__main__":
    # Brak domyślnych wartości
    print("This script is intended to be imported and called from another script.")
