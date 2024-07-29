from PIL import Image
import os
import numpy as np
import pandas as pd
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def calculate_metrics(original_image, compressed_image):
    original_array = np.array(original_image)
    compressed_array = np.array(compressed_image)

    # Ensure both images have the same size
    if original_array.shape != compressed_array.shape:
        compressed_array = np.resize(compressed_array, original_array.shape)

    mse = np.mean((original_array - compressed_array) ** 2)
    if mse == 0:
        psnr_value = 100  # Setting a very high PSNR value instead of infinity
        ssim_value = 1.0
    else:
        psnr_value = psnr(original_array, compressed_array)
        # Determine a suitable win_size
        win_size = min(original_array.shape[0], original_array.shape[1], 7)
        ssim_value = ssim(original_array, compressed_array, win_size=win_size, channel_axis=-1)
    
    return psnr_value, ssim_value

def compress_image(input_file, output_folder, method='lossless', format='jpeg'):
    os.makedirs(output_folder, exist_ok=True)
    base_name = os.path.basename(input_file).rsplit('.', 1)[0]
    
    with Image.open(input_file) as img:
        original_image = img.copy()
        
        if format == 'jpeg':
            if method == 'lossless':
                output_file = os.path.join(output_folder, f"{base_name}_lossless_jpeg.jpg")
                img.save(output_file, 'JPEG', quality=100, optimize=True)
            else:
                output_file = os.path.join(output_folder, f"{base_name}_lossy_jpeg.jpg")
                img.save(output_file, 'JPEG', quality=20, optimize=True)  # Adjust quality for desired compression
        elif format == 'png':
            if method == 'lossless':
                output_file = os.path.join(output_folder, f"{base_name}_lossless_png.png")
                img.save(output_file, 'PNG', optimize=True)
            else:
                output_file = os.path.join(output_folder, f"{base_name}_lossy_png.png")
                img = img.convert('P', palette=Image.ADAPTIVE)  # Convert to palette-based (lossy)
                img.save(output_file, 'PNG', optimize=True)
        elif format == 'jpeg2000':
            if method == 'lossless':
                output_file = os.path.join(output_folder, f"{base_name}_lossless_jpeg2000.jp2")
                img.save(output_file, 'JPEG2000', quality_mode='lossless')
            else:
                output_file = os.path.join(output_folder, f"{base_name}_lossy_jpeg2000.jp2")
                img.save(output_file, 'JPEG2000', quality_layers=[20])  # Adjust layers for desired compression
        else:
            raise ValueError("Unsupported format")
        
        original_size = os.path.getsize(input_file)
        compressed_size = os.path.getsize(output_file)
        compression_ratio = original_size / compressed_size

        with Image.open(output_file) as compressed_img:
            # Resize compressed image to match original image size if necessary
            if original_image.size != compressed_img.size:
                compressed_img = compressed_img.resize(original_image.size)
            psnr_value, ssim_value = calculate_metrics(original_image, compressed_img)
        
        result = {
            "File": output_file,
            "Original Size (bytes)": original_size,
            "Compressed Size (bytes)": compressed_size,
            "Compression Ratio": compression_ratio,
            "PSNR": psnr_value,
            "SSIM": ssim_value
        }
        
        return result

# Example usage:
input_file = '../pictures/2.png'
output_folder = 'output'
result_file = 'results.txt'

formats = ['jpeg', 'png', 'jpeg2000']
methods = ['lossless', 'lossy']

# Clear the results file before writing new results
with open(result_file, 'w') as f:
    f.write("")

results = []

for format in formats:
    for method in methods:
        result = compress_image(input_file, output_folder, method=method, format=format)
        results.append(result)

# Convert results to DataFrame and save to results.txt
df = pd.DataFrame(results)
df.to_csv(result_file, index=False, sep='\t')

print("Compression completed!")
