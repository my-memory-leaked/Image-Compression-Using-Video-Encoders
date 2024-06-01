import os
import shutil
from my_image import MyImage
from encoder import H265Encoder, H265LosslessEncoder
from transformations import row_wise_transform, spiral_transform, hilbert_transform

input_image_path = "pictures/PIA04230.tif"
output_video_path_h265 = "output/output_video_h265_{}.mp4"
output_video_path_h265_lossless = "output/output_video_h265_lossless_{}.mp4"
grid_size = 256
frame_size = 256
output_dir = "output"

def clear_output_dir(output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

def compress_image(lossless=False, transform_name="row_wise", transform=None):
    output_path = output_video_path_h265_lossless.format(transform_name) if lossless else output_video_path_h265.format(transform_name)
    encoder_class = H265LosslessEncoder if lossless else H265Encoder
    
    image = MyImage(input_image_path)
    tiles = image.split_image(grid_size, transform=transform)
    
    # Save tiles for verification
    tiles_output_dir = os.path.join(output_dir, f"tiles_{transform_name}")
    image.save_tiles(tiles, tiles_output_dir)
    
    original_size = sum(tile.nbytes for tile in tiles)
    print(f"Original data size: {original_size} bytes")

    encoder = encoder_class(frame_size)
    encoder.encode_as_video(tiles, output_path)
    if os.path.exists(output_path):
        compressed_size = os.path.getsize(output_path)
        compression_ratio = original_size / compressed_size
        print(f"Video saved to {output_path}")
        print(f"Compressed size: {compressed_size} bytes")
        print(f"Compression ratio ({'H.265 Lossless' if lossless else 'H.265'}): {compression_ratio:.2f}")

if __name__ == "__main__":
    # Clear output directory at the beginning
    clear_output_dir(output_dir)

    transformations = {
        "row_wise": row_wise_transform,
        "spiral": spiral_transform,
        "hilbert": hilbert_transform
    }

    for name, transform in transformations.items():
        print(f"\nCompressing with H.265 (lossy) using {name} transformation...")
        compress_image(lossless=False, transform_name=name, transform=transform)
        print(f"\nCompressing with H.265 (lossless) using {name} transformation...")
        compress_image(lossless=True, transform_name=name, transform=transform)
