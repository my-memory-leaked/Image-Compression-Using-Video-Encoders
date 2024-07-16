import os
import sys
import subprocess
import importlib.util
from PIL import Image
sys.path.append("/home/szymon/Documents/NT/image-compression-using-video-encoders/do-be-deleted")
from decode import decode_video

def get_image_resolution(input_folder, image_template):
    # Construct the path to the first image (e.g., tile_0.png)
    first_image_path = os.path.join(input_folder, image_template % 0)

    # Open the image
    with Image.open(first_image_path) as img:
        width, height = img.size

    return width, height

# Add path to the image-splitter module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../image-splitter')))

splitter_main_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../image-splitter/splitter_main.py'))
if not os.path.exists(splitter_main_path):
    print(f"File not found: {splitter_main_path}")
    sys.exit(1)

spec = importlib.util.spec_from_file_location("splitter_main", splitter_main_path)
splitter_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(splitter_main)

def compress_image(input_folder, output_file, bitrate):
    command = [
        'ffmpeg',
        '-y',
        '-i', os.path.join(input_folder, 'tile_%d.png'),
        '-c:v', 'libvvenc',
        '-preset', 'fast',
        '-b', f'{bitrate}k',
        '-t', '16',
        output_file
    ]
    subprocess.run(command, check=True)

def get_folder_size(folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size

def calculate_compression_ratio(original_size, compressed_size):
    if compressed_size == 0:
        return float('inf')
    return original_size / compressed_size

def compress_to_target_ratio(input_folder, output_file, target_ratio, max_iterations=10):
    original_size = get_folder_size(input_folder)
    bitrate = 1000  # Start with a moderate bitrate in kbps
    step_size = 500  # Initial step size in kbps
    best_bitrate = bitrate
    best_ratio = 0
    error_margin = target_ratio / 10  # Error margin is 1/10 of the target ratio

    for iteration in range(max_iterations):
        compress_image(input_folder, output_file, bitrate)
        compressed_size = os.path.getsize(output_file)
        current_ratio = calculate_compression_ratio(original_size, compressed_size)

        # Logging the sizes and ratios
        print(f"Iteration: {iteration+1}, Bitrate: {bitrate}kbps, Original Size: {original_size}, Compressed Size: {compressed_size}, Current Ratio: {current_ratio:.2f}, Target Ratio: {target_ratio}")

        if abs(current_ratio - target_ratio) <= error_margin:
            best_bitrate = bitrate
            best_ratio = current_ratio
            break

        if current_ratio > target_ratio:
            bitrate += step_size
        else:
            bitrate -= step_size

        # Reduce the step size for finer adjustment as we get closer
        step_size = max(100, step_size // 2)

    print(f"Achieved target compression ratio: {best_ratio:.2f} with bitrate: {best_bitrate}kbps")
    return best_ratio

def main():
    directory = '../../ntwi-zdjecia'
    output_folder = '../output'

    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)

            # Run image_splitter with the provided paths
            splitter_main.run_image_splitter(path, output_folder)

            transformations = ['row_by_row', 'spiral', 'hilbert']
            target_ratios = [10, 30, 100]  # Desired compression ratios

            for transform in transformations:
                input_folder = os.path.join(output_folder, transform)
                if not os.path.exists(input_folder):
                    print(f"Folder {input_folder} does not exist")
                    continue

                for target_ratio in target_ratios:
                    output_file = os.path.join(output_folder, f'output_{transform}_ratio_{target_ratio}.vvc')
                    print(f"\nCompressing with H.266 to achieve {target_ratio}:1 ratio using {transform} transformation...")

                    achieved_ratio = compress_to_target_ratio(input_folder, output_file, target_ratio)

                    original_size = get_folder_size(input_folder)
                    compressed_size = os.path.getsize(output_file)
                    print(f"Original size for {transform} (target ratio {target_ratio}): {original_size} bytes")
                    print(f"Compressed size for {transform} (target ratio {target_ratio}): {compressed_size} bytes")
                    print(f"Achieved compression ratio for {transform} (target ratio {target_ratio}): {achieved_ratio:.2f}")

                    # add ssim and psnr comparison here
                    values = decode_video(output_file, 256, path, f"../../reconstructed_image_{transform}_ratio_{target_ratio}.png")

                    with open("../../results.txt", 'a') as f:
                        f.write(f"{path} transform: {transform} target_ratio: {target_ratio} achieved_ratio: {achieved_ratio:.2f} and PSNR: {values[1]} and SSIM: {values[2]}\n")

if __name__ == "__main__":
    main()
    # create file results.txt before run in project directory!
    # all images can't be compressed at once, split all images into two groups :(
