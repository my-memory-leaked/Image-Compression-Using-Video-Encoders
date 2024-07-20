import os
import subprocess
import cv2

def load_and_resize_images_from_folder(folder, size=(1920, 1080)):
    images = []
    for filename in sorted(os.listdir(folder)):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            img_resized = cv2.resize(img, size)
            images.append(img_resized)
    return images

def generate_frame_sequence(images, total_length):
    x = len(images)
    sequence = images * (total_length // x)
    sequence += images[:total_length % x]
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
        '-vf', 'scale=1920:1080',  # Ensure all frames are the same resolution
        output_file
    ]
    subprocess.run(ffmpeg_command)

def get_file_size(file_path):
    return os.path.getsize(file_path)

def get_total_size(file_paths):
    return sum(get_file_size(path) for path in file_paths)

# Wczytanie obrazów z folderu i przeskalowanie
image_folder = '../pictures'
images = load_and_resize_images_from_folder(image_folder)

# Różne długości sekwencji do testowania
for total_length in [125]:
    # Generowanie i kompresowanie sekwencji
    folder_name = f'sequence_from_images_{total_length}'
    frame_paths = save_frame_sequence(generate_frame_sequence(images, total_length), folder_name)
    output_file = f'{folder_name}.mp4'
    compress_sequence_to_hevc(frame_paths, output_file)

    # Pomiar rozmiaru plików przed i po kompresji
    input_files_size = get_total_size(frame_paths)
    output_file_size = get_file_size(output_file)

    print(f'Total length = {total_length}')
    print(f'Total size of input files: {input_files_size / (1024 * 1024):.2f} MB')
    print(f'Size of output file: {output_file_size / (1024 * 1024):.2f} MB')
    print(f'Compression ratio: {(input_files_size / output_file_size):.2f}\n')
