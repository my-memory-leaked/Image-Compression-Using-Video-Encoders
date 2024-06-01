import os
import cv2
import numpy as np
import imageio_ffmpeg as ffmpeg

class Encoder:
    def __init__(self, frame_size, codec, extra_options=None):
        self.frame_size = frame_size
        self.codec = codec
        self.extra_options = extra_options if extra_options else []

    def encode_as_video(self, tiles, output_path):
        input_path = 'temp_input_frames'
        if not os.path.exists(input_path):
            os.makedirs(input_path)

        # Save tiles as individual frames
        for i, tile in enumerate(tiles):
            tile_resized = cv2.resize(tile, (self.frame_size, self.frame_size), interpolation=cv2.INTER_NEAREST)
            cv2.imwrite(f'{input_path}/frame_{i:04d}.png', cv2.cvtColor(tile_resized, cv2.COLOR_RGB2BGR))

        # Use imageio-ffmpeg to encode frames to video with extra options
        cmd = [
            ffmpeg.get_ffmpeg_exe(), '-y', '-framerate', '1', '-i',
            f'{input_path}/frame_%04d.png', '-c:v', self.codec
        ] + self.extra_options + [output_path]
        
        os.system(' '.join(cmd))

        # Clean up temporary frames
        for file in os.listdir(input_path):
            os.remove(os.path.join(input_path, file))
        os.rmdir(input_path)

    def calculate_compression_ratio(self, original_size, output_path):
        compressed_size = os.path.getsize(output_path)
        return original_size / compressed_size

class H265Encoder(Encoder):
    def __init__(self, frame_size):
        super().__init__(frame_size, 'libx265')

class H265LosslessEncoder(Encoder):
    def __init__(self, frame_size):
        super().__init__(frame_size, 'libx265', ['-x265-params', 'lossless=1'])