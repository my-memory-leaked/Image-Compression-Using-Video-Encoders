from PIL import Image
import os

def compress_image(input_file, output_folder, method='lossless', format='jpeg'):
    os.makedirs(output_folder, exist_ok=True)
    base_name = os.path.basename(input_file).rsplit('.', 1)[0]
    
    with Image.open(input_file) as img:
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
        compression_rate = (original_size - compressed_size) / original_size * 100

    return output_file, compression_rate

# Example usage:
input_file = 'pictures/2.png'
output_folder = 'output'

formats = ['jpeg', 'png', 'jpeg2000']
methods = ['lossless', 'lossy']

for format in formats:
    for method in methods:
        output_file, compression_rate = compress_image(input_file, output_folder, method=method, format=format)
        print(f"Compressed {input_file} to {output_file} with {method} {format} compression. Compression rate: {compression_rate:.2f}%")

print("Compression completed!")
