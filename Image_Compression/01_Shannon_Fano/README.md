# Shannon-Fano Image Compression

A Digital Image Processing project implementing **lossless image compression using Shannon-Fano coding** with a graphical user interface.

## Overview

Shannon-Fano coding is an entropy-based lossless compression technique that assigns shorter binary codes to frequently occurring symbols and longer codes to less frequent symbols.

In this project, grayscale image pixels are treated as symbols and Shannon-Fano coding is used to encode the image data.

## Features

- Graphical User Interface using Tkinter
- Select an image using a file browser
- Automatic grayscale conversion
- Pixel frequency calculation
- Shannon-Fano code generation
- Binary encoding of image pixels
- Compression ratio calculation
- Percentage of space saved calculation
- Display of pixel frequencies and codes
- Save compressed file
- Decompress compressed file
- Reconstruct the original grayscale image
- Image preview
- Lossless reconstruction

## Technologies Used

- Python
- Tkinter
- NumPy
- Pillow

## Project Structure

```text
01_Shannon_Fano/
│
├── shannon_fano.py
├── requirements.txt
├── README.md
│
├── sample_images/
│   └── sample_image.png
│
└── screenshots/
    ├── ui.png
    ├── compressed_output.png
    └── decompressed_output.png