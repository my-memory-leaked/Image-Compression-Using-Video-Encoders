import os
import cv2
import numpy as np
from PIL import Image

def decode_video(video_path, frame_size, grid_size, original_image_path, output_image_path):
    # Get the size of the original image
    original_image = Image.open(original_image_path)
    original_width, original_height = original_image.size
    padded_height = (original_height // grid_size + 1) * grid_size
    padded_width = (original_width // grid_size + 1) * grid_size

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

    # Calculate the number of tiles in the padded image
    num_tiles_vertical = padded_height // grid_size
    num_tiles_horizontal = padded_width // grid_size

    print(f"Padded image shape: ({padded_height}, {padded_width})")
    print(f"Number of tiles - Vertical: {num_tiles_vertical}, Horizontal: {num_tiles_horizontal}")
    print(f"Number of frames extracted: {len(frames)}")

    # Create a blank image
    reconstructed_image = np.zeros((num_tiles_vertical * frame_size, num_tiles_horizontal * frame_size, 3), dtype=np.uint8)

    # Place each frame into the reconstructed image
    for i, frame in enumerate(frames):
        row = (i // num_tiles_horizontal) * frame_size
        col = (i % num_tiles_horizontal) * frame_size
        print(f"Placing frame {i} at row {row}, col {col}")
        reconstructed_image[row:row+frame_size, col:col+frame_size] = frame

    # Crop the reconstructed image to the original dimensions
    original_image = reconstructed_image[:original_height, :original_width]

    # Save the reconstructed image
    cv2.imwrite(output_image_path, cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR))
    print(f"Reconstructed image saved to {output_image_path}")

if __name__ == "__main__":
    video_path = "output/output_video_h265.mp4"
    output_image_path = "output/reconstructed_image.png"
    frame_size = 256
    grid_size = 256  # Same as the one used in encoding
    original_image_path = "pictures/Canon-5DMarkII-Shotkit-4.CR2"

    decode_video(video_path, frame_size, grid_size, original_image_path, output_image_path)
