import os
import subprocess
import cv2
import numpy as np

def load_image_from_folder(folder, filename):
    filepath = os.path.join(folder, filename)
    image = cv2.imread(filepath)
    if image is None:
        raise FileNotFoundError(f"Image {filename} not found in folder {folder}")
    return image

def create_pixel_changing_sequence(image, num_frames):
    height, width, _ = image.shape
    sequence = []
    for i in range(num_frames):
        frame = image.copy()
        x = i % width
        y = (i // width) % height
        frame[y, x] = [255, 0, 0]  # Zmieniamy piksel na czerwony
        sequence.append(frame)
    return sequence

def save_frame_sequence(sequence, folder_name):
    os.makedirs(folder_name, exist_ok=True)
    frame_paths = []
    for i, frame in enumerate(sequence):
        frame_path = os.path.join(folder_name, f'frame_{i:04d}.png')
        cv2.imwrite(frame_path, frame)
        frame_paths.append(frame_path)
    return frame_paths

def compress_sequence_to_hevc(frame_paths, output_file):
    input_pattern = os.path.join(os.path.dirname(frame_paths[0]), 'frame_%04d.png')
    ffmpeg_command = [
        'ffmpeg',
        '-y',
        '-framerate', '25', 
        '-i', input_pattern,
        '-c:v', 'libx265',
        '-preset', 'medium',
        '-x265-params', 'lossless=1',
        output_file
    ]
    subprocess.run(ffmpeg_command)

def get_file_size(file_path):
    return os.path.getsize(file_path)

def get_total_size(file_paths):
    return sum(get_file_size(path) for path in file_paths)

# Wczytanie obrazu z folderu
image_folder = '../pictures'
image_filename = '1.png'  # Wskaż odpowiedni plik obrazu
image = load_image_from_folder(image_folder, image_filename)

# Generowanie sekwencji klatek
total_length = 10
sequence = create_pixel_changing_sequence(image, total_length)

# Zapisanie sekwencji klatek
folder_name = 'pixel_changing_sequence'
frame_paths = save_frame_sequence(sequence, folder_name)
output_file = f'{folder_name}.mp4'
compress_sequence_to_hevc(frame_paths, output_file)

# Pomiar rozmiaru plików przed i po kompresji
input_files_size = get_total_size(frame_paths)
output_file_size = get_file_size(output_file)

print(f'Total length = {total_length}')
print(f'Total size of input files: {input_files_size / (1024 * 1024):.2f} MB')
print(f'Size of output file: {output_file_size / (1024 * 1024):.2f} MB')
print(f'Compression ratio: {(input_files_size / output_file_size):.2f}')
