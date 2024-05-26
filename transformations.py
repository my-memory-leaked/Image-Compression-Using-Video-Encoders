import numpy as np
from hilbertcurve.hilbertcurve import HilbertCurve

def row_wise_transform(image):
    return image.flatten()

def spiral_transform(image):
    h, w, c = image.shape
    result = []
    for channel in range(c):
        channel_data = image[:, :, channel]
        channel_result = []
        while channel_data.size:
            channel_result.extend(channel_data[0])
            channel_data = channel_data[1:].T[::-1]
        result.append(np.array(channel_result).reshape(h, w))
    return np.stack(result, axis=-1)

def hilbert_transform(image):
    h, w, c = image.shape
    max_dim = max(h, w)
    p = int(np.ceil(np.log2(max_dim)))
    hilbert_curve = HilbertCurve(p, 2)
    num_points = 2 ** p

    # Generate Hilbert curve points and filter out-of-bound indices
    points = np.array([hilbert_curve.point_from_distance(i) for i in range(num_points ** 2)])
    valid_points = points[(points[:, 0] < h) & (points[:, 1] < w)]

    result = []
    for channel in range(c):
        flat_image = image[:, :, channel].flatten()
        transformed_channel = flat_image[valid_points[:, 0] * w + valid_points[:, 1]]
        result.append(transformed_channel.reshape(h, w))
        
    return np.stack(result, axis=-1)
