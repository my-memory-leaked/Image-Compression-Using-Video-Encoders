import os
import sys
import subprocess
import importlib.util

# Dodanie ścieżki do modułu image-splitter
splitter_main_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../image-splitter/splitter_main.py'))
if not os.path.exists(splitter_main_path):
    print(f"File not found: {splitter_main_path}")
    sys.exit(1)

spec = importlib.util.spec_from_file_location("splitter_main", splitter_main_path)
splitter_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(splitter_main)

def compress_image(input_folder, output_file, lossless=True):
    crf_value = 0 if lossless else 28  # CRF 0 means lossless, 28 is a good tradeoff for lossy
    command = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-i', os.path.join(input_folder, 'tile_%d.png'),  # Input pattern
        '-c:v', 'libx265',  # Codec
        '-preset', 'fast',  # Encoding speed (tradeoff between speed and compression)
        '-x265-params', f'crf={crf_value}',  # CRF value for compression
        output_file  # Output file
    ]
    subprocess.run(command, check=True)

def get_folder_size(folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def main():
    input_image_path = '../pictures/PIA04230.tif'  # Zaktualizowana ścieżka do obrazu
    output_folder = '../output'

    # Uruchomienie image_splitter z przekazanymi ścieżkami
    splitter_main.run_image_splitter(input_image_path, output_folder)

    transformations = ['row_by_row', 'spiral', 'hilbert']

    for transform in transformations:
        input_folder = os.path.join(output_folder, transform)
        if not os.path.exists(input_folder):
            print(f"Folder {input_folder} does not exist")
            continue

        for lossy in [True, False]:
            mode = "lossless" if not lossy else "lossy"
            output_file = os.path.join(output_folder, f'output_{transform}_{mode}.hevc')

            print(f"\nCompressing with H.265 ({mode}) using {transform} transformation...")
            compress_image(input_folder, output_file, lossless=not lossy)

            # Calculate compression ratio
            original_size = get_folder_size(input_folder)
            compressed_size = os.path.getsize(output_file)
            compression_ratio = original_size / compressed_size if compressed_size != 0 else float('inf')
            print(f"Compression ratio for {transform} ({mode}): {compression_ratio:.2f}")

if __name__ == "__main__":
    main()
