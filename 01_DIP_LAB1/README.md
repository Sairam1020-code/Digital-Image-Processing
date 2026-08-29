# DIP Lab 1 — RGB, Grayscale and Binary Image Processing

This project demonstrates basic digital image processing operations using Python, OpenCV, NumPy, and Matplotlib.

## Objectives

- Read a color image using OpenCV
- Convert a BGR image to RGB format
- Separate the Red, Green, and Blue color channels
- Display individual RGB channel intensities
- Display the actual Red, Green, and Blue layers
- Convert the color image into a grayscale image
- Convert the grayscale image into a black-and-white binary image using thresholding

## Technologies Used

- Python
- OpenCV
- NumPy
- Matplotlib

## Processing Steps

1. Read the input image.
2. Convert the image from BGR to RGB.
3. Extract the Red, Green, and Blue channel intensities.
4. Create separate RGB layer images.
5. Convert the image to grayscale.
6. Apply binary thresholding with a threshold value of 128.
7. Display all results in a single figure.

## Outputs

The program displays:

- Original Image
- Red Intensity
- Actual Red Layer
- Green Intensity
- Actual Green Layer
- Blue Intensity
- Actual Blue Layer
- Grayscale Image
- Black and White Image

## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt