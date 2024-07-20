import os
import cv2
import numpy as np
from PIL import Image
from skimage.metrics import peak_signal_noise_ratio as compare_psnr
from skimage.metrics import structural_similarity as compare_ssim
import rawpy

def read_image(image_path):
    if image_path.lower().endswith('.cr2'):
        with rawpy.imread(image_path) as raw:
            return raw.postprocess()
    else:
        return cv2.imread(image_path)

def decode_video(video_path, frame_size, original_image_path, output_image_path):
    # Get the size of the original image
    original_img = read_image(original_image_path)
    if original_img is None:
        raise ValueError(f"Failed to read the original image from {original_image_path}")
    if original_image_path.lower().endswith('.cr2'):
        original_height, original_width, _ = original_img.shape
    else:
        original_image = Image.open(original_image_path)
        original_width, original_height = original_image.size

    num_tiles_vertical = (original_height + frame_size - 1) // frame_size
    num_tiles_horizontal = (original_width + frame_size - 1) // frame_size

    padded_height = num_tiles_vertical * frame_size
    padded_width = num_tiles_horizontal * frame_size

    cap = cv2.VideoCapture(video_path)
    
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    cap.release()

    if not frames:
        raise ValueError("No frames extracted from the video.")

    if len(frames) != num_tiles_vertical * num_tiles_horizontal:
        print(f"Warning: Number of frames ({len(frames)}) does not match grid size ({num_tiles_vertical * num_tiles_horizontal}).")

    # Create a blank image
    reconstructed_image = np.zeros((padded_height, padded_width, 3), dtype=np.uint8)

    # Place each frame into the reconstructed image column by column
    for i, frame in enumerate(frames):
        col = (i // num_tiles_vertical) * frame_size
        row = (i % num_tiles_vertical) * frame_size
        reconstructed_image[row:row+frame_size, col:col+frame_size] = frame

    # Crop the reconstructed image to the original dimensions
    reconstructed_image = reconstructed_image[:original_height, :original_width]

    # Save the reconstructed image
    cv2.imwrite(output_image_path, cv2.cvtColor(reconstructed_image, cv2.COLOR_RGB2BGR))
    print(f"Reconstructed image saved to {output_image_path}")

    # Re-read the saved reconstructed image to ensure correctness
    reconstructed_img = cv2.imread(output_image_path)
    if reconstructed_img is None:
        raise ValueError(f"Failed to read the reconstructed image from {output_image_path}")

    # Calculate PSNR and SSIM
    psnr_value = compare_psnr(original_img, reconstructed_img)
    
    # Calculate a suitable win_size
    min_dim = min(original_img.shape[0], original_img.shape[1], reconstructed_img.shape[0], reconstructed_img.shape[1])
    win_size = min(7, min_dim)
    
    # Ensure win_size is odd and less than or equal to the smallest image dimension
    if win_size % 2 == 0:
        win_size -= 1

    win_size = max(3, min(win_size, min(original_img.shape[0], original_img.shape[1], 7)))

    print(f"Using win_size: {win_size}")

    ssim_value, _ = compare_ssim(original_img, reconstructed_img, full=True, multichannel=True, win_size=win_size, channel_axis=2)

    print(f"PSNR: {psnr_value}")
    print(f"SSIM: {ssim_value}")

if __name__ == "__main__":
    video_path = "../output/output_column_by_column_lossless.hevc"
    output_image_path = "../output/reconstructed_image_column_by_column_lossless.png"
    frame_size = 256
    original_image_path = "../pictures/14.png"

    decode_video(video_path, frame_size, original_image_path, output_image_path)
