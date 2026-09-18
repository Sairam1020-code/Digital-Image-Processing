import cv2
import matplotlib.pyplot as plt
import numpy as np

img =cv2.imread("Sample_Photo.jpg")

img_rgb =cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

R=img_rgb[:,:,0]
G=img_rgb[:,:,1]
B=img_rgb[:,:,2]

red_image=np.zeros_like(img_rgb)
red_image[:,:,0]=R

green_image =np.zeros_like(img_rgb)
green_image[:,:,1]=G

blue_image = np.zeros_like(img_rgb)
blue_image[:,:,2] = B

gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

_,bw=cv2.threshold(gray,128,255,cv2.THRESH_BINARY)

plt.figure(figsize=(16,10))

plt.subplot(3,3,1)
plt.imshow(img_rgb)
plt.title("Original Image")
plt.axis("off")

plt.subplot(3,3,2)
plt.imshow(R, cmap="gray")
plt.title("Red Intensity")
plt.axis("off")

plt.subplot(3,3,3)
plt.imshow(red_image)
plt.title("Actual Red Layer")
plt.axis("off")

plt.subplot(3,3,4)
plt.imshow(G, cmap="gray")
plt.title("Green Intensity")
plt.axis("off")

plt.subplot(3,3,5)
plt.imshow(green_image)
plt.title("Actual Green Layer")
plt.axis("off")

plt.subplot(3,3,6)
plt.imshow(B, cmap="gray")
plt.title("Blue Intensity")
plt.axis("off")

plt.subplot(3,3,7)
plt.imshow(blue_image)
plt.title("Actual Blue Layer")
plt.axis("off")

plt.subplot(3,3,8)
plt.imshow(gray, cmap="gray")
plt.title("Grayscale Image")
plt.axis("off")

plt.subplot(3,3,9)
plt.imshow(bw, cmap="gray")
plt.title("Black and White Image")
plt.axis("off")

plt.tight_layout()
plt.show()