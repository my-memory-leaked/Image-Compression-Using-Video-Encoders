
# H265 HEVC Video Compression Project

This project implements video compression using external libraries in Python, specifically leveraging the `imageio_ffmpeg` library, which integrates the FFmpeg tool. FFmpeg is a popular open-source tool used for multimedia processing, including video encoding and decoding.

## Project Overview

The project focuses on comparing different video compression algorithms and their efficiency, especially using the H.265 (HEVC) codec. The compression methods include:

- Row-wise processing
- Column-wise processing
- Spiral processing
- Hilbert curve processing

### Features

- **Lossless and Lossy Compression**: Conducted tests for both lossless and lossy compression on a set of images using the HEVC encoder.
- **Algorithm Comparison**: Compared the efficiency of HEVC with traditional compression methods such as JPEG, PNG, and JPEG 2000.
- **Compression Ratios**: Investigated various compression ratios (10:1, 30:1, 100:1) and their impact on image quality.

### Results

- **Higher Compression Ratios**: HEVC provided higher compression ratios compared to JPEG, PNG, and JPEG 2000.
- **Algorithm Impact**: The choice of algorithm (row-wise, spiral, Hilbert) had minimal impact on the compression efficiency of HEVC.
- **Efficiency**: HEVC was found to be more efficient for formats like BMP, TIFF, and CR2 compared to traditional methods.

## Getting Started

### Prerequisites

- Python 3.x
- `imageio_ffmpeg` library
- FFmpeg tool

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
