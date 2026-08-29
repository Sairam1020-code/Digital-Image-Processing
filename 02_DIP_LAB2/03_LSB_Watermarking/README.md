# LSB-Based Digital Image Watermarking using Python

## Overview

This project demonstrates digital image watermarking using the Least Significant Bit (LSB) technique.

The application allows a user to add a visible watermark to an image and also embed hidden watermark text inside the least significant bit of the blue color channel. The hidden watermark can later be extracted from the watermarked image.

A graphical user interface is provided using Tkinter.

## Features

- Open and display an image
- Add custom watermark text
- Choose watermark color
- Adjust watermark brightness
- Adjust watermark opacity
- Change watermark font size
- Select watermark position
- Add an optional background box
- Preview the visible watermark
- Embed hidden text using LSB
- Extract the hidden watermark
- Display LSB embedding status
- Show available watermark capacity
- Save the watermarked image
- Reset the application

## LSB Watermarking

The Least Significant Bit technique hides data by modifying the lowest bit of pixel values.

In this project, the hidden watermark text is embedded in:

- Blue color channel
- Bit 0 (Least Significant Bit)

A 32-bit header is used to store the length of the hidden text, followed by the watermark message bits.

## Visible Watermark

Along with hidden LSB data, the project also supports a visible watermark.

The user can customize:

- Text
- Color
- Brightness
- Opacity
- Font size
- Position
- Background box

## Technologies Used

- Python
- OpenCV
- NumPy
- Pillow
- Tkinter

## Supported Image Formats

For opening images:

- PNG
- JPG / JPEG
- BMP
- TIFF

For saving watermarked images, lossless formats are recommended:

- PNG
- BMP
- TIFF

JPEG is not recommended for the final LSB-embedded image because lossy compression can modify pixel values and destroy the hidden watermark.

## How to Run

Install the required packages:

```bash
pip install -r requirements.txt