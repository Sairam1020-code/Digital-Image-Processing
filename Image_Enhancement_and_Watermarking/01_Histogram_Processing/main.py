import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import matplotlib.pyplot as plt


class HistogramImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Image Processing - Histogram Techniques")
        self.root.geometry("1200x750")
        self.root.configure(bg="#eeeeee")

        self.original_image = None
        self.processed_image = None

        title = tk.Label(
            root,
            text="Digital Image Processing - Histogram Processing",
            font=("Arial", 20, "bold"),
            bg="#eeeeee"
        )
        title.pack(pady=10)

        button_frame = tk.Frame(root, bg="#eeeeee")
        button_frame.pack(pady=5)

        tk.Button(
            button_frame,
            text="Open Image",
            command=self.open_image,
            width=15
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Save Image",
            command=self.save_image,
            width=15
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_image,
            width=15
        ).grid(row=0, column=2, padx=5)

        process_frame = tk.LabelFrame(
            root,
            text="Histogram Techniques",
            font=("Arial", 12, "bold"),
            bg="#eeeeee"
        )
        process_frame.pack(pady=10)

        tk.Button(
            process_frame,
            text="Global Histogram Equalization",
            command=self.global_equalization,
            width=28
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            process_frame,
            text="Adaptive / Local Histogram",
            command=self.adaptive_histogram,
            width=28
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            process_frame,
            text="CLAHE",
            command=self.clahe,
            width=28
        ).grid(row=0, column=2, padx=5, pady=5)

        tk.Button(
            process_frame,
            text="Increase Contrast",
            command=self.increase_contrast,
            width=28
        ).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            process_frame,
            text="Decrease Contrast",
            command=self.decrease_contrast,
            width=28
        ).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            process_frame,
            text="Show Histogram",
            command=self.show_histogram,
            width=28
        ).grid(row=1, column=2, padx=5, pady=5)

        slider_frame = tk.Frame(root, bg="#eeeeee")
        slider_frame.pack(pady=5)

        tk.Label(
            slider_frame,
            text="Contrast:",
            font=("Arial", 11, "bold"),
            bg="#eeeeee"
        ).pack(side=tk.LEFT)

        self.contrast_slider = tk.Scale(
            slider_frame,
            from_=0.5,
            to=3.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            length=300,
            bg="#eeeeee"
        )
        self.contrast_slider.set(1.5)
        self.contrast_slider.pack(side=tk.LEFT, padx=10)

        tk.Button(
            slider_frame,
            text="Apply Contrast",
            command=self.apply_contrast_slider,
            width=18
        ).pack(side=tk.LEFT)

        image_frame = tk.Frame(root, bg="#eeeeee")
        image_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=10
        )

        original_frame = tk.LabelFrame(
            image_frame,
            text="Original Image",
            font=("Arial", 12, "bold"),
            bg="#eeeeee"
        )
        original_frame.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=10
        )

        self.original_label = tk.Label(
            original_frame,
            text="Open an image",
            bg="#eeeeee"
        )
        self.original_label.pack(expand=True)

        processed_frame = tk.LabelFrame(
            image_frame,
            text="Processed Image",
            font=("Arial", 12, "bold"),
            bg="#eeeeee"
        )
        processed_frame.pack(
            side=tk.RIGHT,
            fill=tk.BOTH,
            expand=True,
            padx=10
        )

        self.processed_label = tk.Label(
            processed_frame,
            text="Processed image will appear here",
            bg="#eeeeee"
        )
        self.processed_label.pack(expand=True)

        self.status = tk.Label(
            root,
            text="Status: Ready",
            anchor="w",
            bg="#dddddd",
            font=("Arial", 10)
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")
            ]
        )

        if not file_path:
            return

        self.original_image = cv2.imread(file_path)

        if self.original_image is None:
            messagebox.showerror("Error", "Unable to open image.")
            return

        self.processed_image = self.original_image.copy()
        self.display_images()
        self.status.config(text="Status: Image loaded successfully")

    def display_images(self):
        if self.original_image is not None:
            original_rgb = cv2.cvtColor(
                self.original_image,
                cv2.COLOR_BGR2RGB
            )

            img = Image.fromarray(original_rgb)
            img.thumbnail((500, 400))

            self.original_photo = ImageTk.PhotoImage(img)
            self.original_label.config(
                image=self.original_photo,
                text=""
            )

        if self.processed_image is not None:
            processed_rgb = cv2.cvtColor(
                self.processed_image,
                cv2.COLOR_BGR2RGB
            )

            img = Image.fromarray(processed_rgb)
            img.thumbnail((500, 400))

            self.processed_photo = ImageTk.PhotoImage(img)
            self.processed_label.config(
                image=self.processed_photo,
                text=""
            )

    def get_gray(self):
        if self.original_image is None:
            messagebox.showwarning(
                "Warning",
                "Please open an image first."
            )
            return None

        return cv2.cvtColor(
            self.original_image,
            cv2.COLOR_BGR2GRAY
        )

    def global_equalization(self):
        gray = self.get_gray()

        if gray is None:
            return

        equalized = cv2.equalizeHist(gray)

        self.processed_image = cv2.cvtColor(
            equalized,
            cv2.COLOR_GRAY2BGR
        )

        self.display_images()
        self.status.config(
            text="Status: Global Histogram Equalization applied"
        )

    def adaptive_histogram(self):
        gray = self.get_gray()

        if gray is None:
            return

        adaptive = cv2.createCLAHE(
            clipLimit=1.0,
            tileGridSize=(8, 8)
        )

        result = adaptive.apply(gray)

        self.processed_image = cv2.cvtColor(
            result,
            cv2.COLOR_GRAY2BGR
        )

        self.display_images()
        self.status.config(
            text="Status: Adaptive / Local Histogram applied"
        )

    def clahe(self):
        gray = self.get_gray()

        if gray is None:
            return

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )

        result = clahe.apply(gray)

        self.processed_image = cv2.cvtColor(
            result,
            cv2.COLOR_GRAY2BGR
        )

        self.display_images()
        self.status.config(text="Status: CLAHE applied")

    def increase_contrast(self):
        if self.original_image is None:
            messagebox.showwarning(
                "Warning",
                "Please open an image first."
            )
            return

        self.processed_image = cv2.convertScaleAbs(
            self.original_image,
            alpha=1.5,
            beta=0
        )

        self.display_images()
        self.status.config(text="Status: Contrast increased")

    def decrease_contrast(self):
        if self.original_image is None:
            messagebox.showwarning(
                "Warning",
                "Please open an image first."
            )
            return

        self.processed_image = cv2.convertScaleAbs(
            self.original_image,
            alpha=0.5,
            beta=0
        )

        self.display_images()
        self.status.config(text="Status: Contrast decreased")

    def apply_contrast_slider(self):
        if self.original_image is None:
            messagebox.showwarning(
                "Warning",
                "Please open an image first."
            )
            return

        alpha = self.contrast_slider.get()

        self.processed_image = cv2.convertScaleAbs(
            self.original_image,
            alpha=alpha,
            beta=0
        )

        self.display_images()
        self.status.config(
            text=f"Status: Contrast set to {alpha}"
        )

    def show_histogram(self):
        if self.original_image is None:
            messagebox.showwarning(
                "Warning",
                "Please open an image first."
            )
            return

        original_gray = cv2.cvtColor(
            self.original_image,
            cv2.COLOR_BGR2GRAY
        )

        processed_gray = cv2.cvtColor(
            self.processed_image,
            cv2.COLOR_BGR2GRAY
        )

        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)
        plt.hist(
            original_gray.ravel(),
            bins=256,
            range=[0, 256]
        )
        plt.title("Original Histogram")
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")

        plt.subplot(1, 2, 2)
        plt.hist(
            processed_gray.ravel(),
            bins=256,
            range=[0, 256]
        )
        plt.title("Processed Histogram")
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")

        plt.tight_layout()
        plt.show()

    def reset_image(self):
        if self.original_image is None:
            return

        self.processed_image = self.original_image.copy()
        self.display_images()
        self.status.config(text="Status: Image reset")

    def save_image(self):
        if self.processed_image is None:
            messagebox.showwarning(
                "Warning",
                "No processed image available."
            )
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("BMP Image", "*.bmp")
            ]
        )

        if not file_path:
            return

        cv2.imwrite(file_path, self.processed_image)

        messagebox.showinfo(
            "Success",
            "Image saved successfully!"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = HistogramImageApp(root)
    root.mainloop()