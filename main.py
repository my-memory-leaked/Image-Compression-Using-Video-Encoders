import os
from my_image import MyImage
from encoder import H265Encoder, H265LosslessEncoder

# input_image_path = "pictures/Canon-5DMarkII-Shotkit-4.CR2"
input_image_path = "pictures/2.png"

output_video_path_h265 = "output/output_video_h265.mp4"
output_video_path_h265_lossless = "output/output_video_h265_lossless.mp4"
grid_size = 256
frame_size = 256

def compress_image(lossless=False):
    output_path = output_video_path_h265_lossless if lossless else output_video_path_h265
    encoder_class = H265LosslessEncoder if lossless else H265Encoder

    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    image = MyImage(input_image_path)
        
    tiles = image.split_image(grid_size)
    
    # Calculate original data size
    original_size = sum(tile.nbytes for tile in tiles)
    print(f"Original data size: {original_size} bytes")

    # Encoding
    encoder = encoder_class(frame_size)
    encoder.encode_as_video(tiles, output_path)
    if os.path.exists(output_path):
        compression_ratio = encoder.calculate_compression_ratio(original_size, output_path)
        print(f"Video saved to {output_path}")
        print(f"Compression ratio ({'H.265 Lossless' if lossless else 'H.265'}): {compression_ratio:.2f}")

if __name__ == "__main__":
    print("Compressing with H.265 (lossy)...")
    compress_image(lossless=False)
    print("\nCompressing with H.265 (lossless)...")
    compress_image(lossless=True)
