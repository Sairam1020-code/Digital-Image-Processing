# Digital Image Processing Using Python

A collection of Digital Image Processing experiments and projects implemented using Python, OpenCV, NumPy, Matplotlib, Pillow, and Tkinter.

## Technologies

- Python
- OpenCV
- NumPy
- Matplotlib
- Pillow
- Tkinter

## Experiments and Projects

### 1. Tambola Ticket Generator

- Automatic Tambola ticket generation
- Random number arrangement
- Ticket visualization using Python

### 2. DIP Lab 1

- RGB color channel separation
- Grayscale image conversion
- Black and white (binary) image conversion

### 3. DIP Lab 2

#### 3.1 Interactive Histogram Analysis & Enhancement

- Original image and histogram
- Global histogram
- Local histogram
- Adaptive histogram
- CLAHE enhancement
- Histogram increase and decrease
- Processed histogram

#### 3.2 Bit Plane Slicing & Image Reconstruction

- 8-bit plane decomposition
- Bit planes 7 to 0
- Selected bit planes
- Image reconstruction
- Comparison of original and reconstructed images

#### 3.3 LSB-Based Digital Image Watermarking

- LSB plane extraction
- Watermark embedding
- Watermark extraction
- Customized watermark
- Watermarked image analysis
- Brightness and color variations
- Watermark comparison

### 4. DIP Lab 3

#### 4.1 Shannon-Fano Image Compression

- Shannon-Fano coding
- Pixel frequency analysis
- Variable-length binary code generation
- Grayscale image compression
- Lossless image decompression
- Compression ratio calculation
- Space saved calculation
- Pixel frequency and code visualization
- Graphical User Interface (GUI)

#### 4.2 Huffman Image Compression

- Huffman tree construction
- Pixel frequency analysis
- Huffman code generation
- Variable-length binary coding
- Grayscale image compression
- Lossless image decompression
- Compression ratio calculation
- Space saved calculation
- Pixel frequency and code visualization
- Graphical User Interface (GUI)

## Repository Structure

```text
Digital-Image-Processing/
│
├── 01_DIP_LAB1/
│   ├── dip_lab1.py
│   ├── Output_Lab1.png
│   ├── README.md
│   ├── requirements.txt
│   └── Sample_Photo.jpg
│
├── 02_DIP_LAB2/
│   │
│   ├── 01_Histogram_Processing/
│   │   ├── sample_images/
│   │   ├── screenshots/
│   │   ├── main.py
│   │   ├── README.md
│   │   └── requirements.txt
│   │
│   ├── 02_Bit_Plane_Slicing/
│   │   ├── sample_images/
│   │   ├── screenshots/
│   │   ├── main.py
│   │   ├── README.md
│   │   └── requirements.txt
│   │
│   └── 03_LSB_Watermarking/
│       ├── sample_images/
│       ├── screenshots/
│       ├── main.py
│       ├── README.md
│       └── requirements.txt
│
├── 03_DIP_LAB3/
│   │
│   ├── 01_Shannon_Fano/
│   │   ├── sample_images/
│   │   ├── screenshots/
│   │   ├── main.py
│   │   ├── README.md
│   │   └── requirements.txt
│   │
│   └── 02_Huffman/
│       ├── sample_images/
│       ├── screenshots/
│       ├── main.py
│       ├── README.md
│       └── requirements.txt
│
├── Tambola_Ticket_Generator/
│   ├── Output_Tambola-Ticket.png
│   ├── README.md
│   ├── requirements.txt
│   └── tambola_ticket.py
│
├── README.md
└── requirements.txt