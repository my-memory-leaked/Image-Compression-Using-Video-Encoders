import os
from my_image import MyImage
from encoder import Encoder

input_image_path = "pictures/1.png"
output_video_path = "output/output_video.avi"
grid_size = 256
frame_size = 256

def main():
    output_dir = os.path.dirname(output_video_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    image = MyImage(input_image_path)
    image.show()
    
    tiles = image.split_image(grid_size)
    
    encoder = Encoder(frame_size)
    encoder.encode_as_video(tiles, output_video_path)
    
    print(f"Video saved to {output_video_path}")

if __name__ == "__main__":
    main()
