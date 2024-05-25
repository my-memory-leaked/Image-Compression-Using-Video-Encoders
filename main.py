import os
from my_image import MyImage
from encoder import H265Encoder

input_image_path = "pictures/Canon-5DMarkII-Shotkit-4.CR2"
output_video_path_h265 = "output/output_video_h265.mp4"
grid_size = 256
frame_size = 256

def main():
    output_dir = os.path.dirname(output_video_path_h265)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    image = MyImage(input_image_path)
    # image.show()
    
    tiles = image.split_image(grid_size)
    
    # Calculate original data size
    original_size = sum(tile.nbytes for tile in tiles)
    print(f"Original data size: {original_size} bytes")

    # H.265 encoding
    encoder_h265 = H265Encoder(frame_size)
    encoder_h265.encode_as_video(tiles, output_video_path_h265)
    if os.path.exists(output_video_path_h265):
        compression_ratio_h265 = encoder_h265.calculate_compression_ratio(original_size, output_video_path_h265)
        print(f"Video saved to {output_video_path_h265}")
        print(f"Compression ratio (H.265): {compression_ratio_h265:.2f}")

if __name__ == "__main__":
    main()
