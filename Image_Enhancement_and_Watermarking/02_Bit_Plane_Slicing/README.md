# Bit Plane Slicing & Image Reconstruction using Python

## Overview

This project demonstrates Bit Plane Slicing and Image Reconstruction for 8-bit grayscale images.

The application decomposes a grayscale image into its eight individual bit planes, from Bit 7 (MSB) to Bit 0 (LSB). Users can view individual bit planes and reconstruct the image using selected bit planes.

A graphical user interface is provided using Tkinter.

## Features

- Open and display an image
- Automatic grayscale conversion
- Extract Bit Planes 7 to 0
- Display all eight bit planes
- View individual bit planes
- Select multiple bit planes
- Reconstruct an image using selected bit planes
- Compare original and reconstructed images
- Save the processed result
- Reset the application
- Simple graphical user interface

## Bit Plane Slicing

An 8-bit grayscale image contains pixel values from 0 to 255.

Each pixel is represented using 8 binary bits:

- Bit 7 - Most Significant Bit (MSB)
- Bit 6
- Bit 5
- Bit 4
- Bit 3
- Bit 2
- Bit 1
- Bit 0 - Least Significant Bit (LSB)

The image is decomposed into eight binary images corresponding to these individual bit positions.

For bit position `b`, the bit plane is extracted using:

```python
plane = (gray >> b) & 1