# Interactive Histogram Analysis & Enhancement using Python

## Overview

This project implements different histogram processing and image enhancement techniques using Python, OpenCV, and Matplotlib.

A simple graphical user interface is provided using Tkinter, allowing an image to be loaded, processed, displayed, and saved.

## Main Features

- Open and display an image
- Global Histogram Equalization
- Adaptive / Local Histogram Processing
- CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Increase image contrast
- Decrease image contrast
- Adjustable contrast using a slider
- Display original and processed histograms
- Save the processed image
- Reset the processed image

## Technologies Used

- Python
- OpenCV
- NumPy
- Matplotlib
- Tkinter
- Pillow

## Histogram Processing Techniques

### Global Histogram Equalization

Improves the overall contrast of a grayscale image by redistributing pixel intensity values.

### Adaptive / Local Histogram

Processes different regions of an image separately to improve local contrast.

### CLAHE

CLAHE improves local contrast while limiting excessive amplification of noise.

### Contrast Adjustment

The contrast of the image can be increased or decreased using scaling factors. A slider is also provided for interactive contrast adjustment.

## Output

The application displays:

- Original Image
- Processed Image
- Original Histogram
- Processed Histogram

## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt