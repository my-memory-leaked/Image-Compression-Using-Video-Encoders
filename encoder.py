import cv2
import numpy as np

class Encoder:
    def __init__(self, frame_size):
        self.frame_size = frame_size

    def encode_as_video(self, tiles, output_path):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, fourcc, 1.0, (self.frame_size, self.frame_size))

        for tile in tiles:
            tile_resized = cv2.resize(tile, (self.frame_size, self.frame_size), interpolation=cv2.INTER_NEAREST)
            out.write(tile_resized)

        out.release()
