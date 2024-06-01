import os
import sys
from utils.helper import clear_output_folder
from utils.row_by_row import slice_image_row_by_row
from utils.spiral import slice_image_spiral
from utils.hilbert import slice_image_hilbert

def main():
    input_image_path = '../pictures/PIA04230.tif'  # Zaktualizowana ścieżka do obrazu
    output_folder = 'output'

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
    main()
