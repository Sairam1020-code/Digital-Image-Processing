import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np


class BitPlaneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bit Plane Slicing - Digital Image Processing")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg="#eef2f7")

        self.gray = None
        self.original = None
        self.result = None

        self.original_photo = None
        self.result_photo = None
        self.plane_photos = {}

        self.check_vars = {}

        self.create_interface()

    def create_interface(self):
        header = tk.Frame(self.root, bg="#2563eb", height=75)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="BIT PLANE SLICING",
            font=("Segoe UI", 22, "bold"),
            fg="white",
            bg="#2563eb"
        ).pack(pady=(12, 0))

        tk.Label(
            header,
            text="8-Bit Decomposition and Image Reconstruction",
            font=("Segoe UI", 10),
            fg="#dbeafe",
            bg="#2563eb"
        ).pack()

        main = tk.Frame(self.root, bg="#eef2f7")
        main.pack(fill="both", expand=True, padx=12, pady=12)

        controls = tk.Frame(
            main,
            bg="white",
            width=220,
            bd=1,
            relief="solid"
        )
        controls.pack(side="left", fill="y", padx=(0, 12))
        controls.pack_propagate(False)

        tk.Label(
            controls,
            text="CONTROLS",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg="#172033"
        ).pack(pady=15)

        self.make_button(
            controls,
            "Open Image",
            self.open_image,
            "#2563eb"
        ).pack(fill="x", padx=15, pady=4)

        self.make_button(
            controls,
            "Reset",
            self.reset,
            "#64748b"
        ).pack(fill="x", padx=15, pady=4)

        tk.Frame(
            controls,
            height=1,
            bg="#e2e8f0"
        ).pack(fill="x", padx=15, pady=12)

        tk.Label(
            controls,
            text="SELECT BIT PLANES",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#475569"
        ).pack(pady=(0, 8))

        for bit in range(7, -1, -1):
            var = tk.BooleanVar()
            self.check_vars[bit] = var

            tk.Checkbutton(
                controls,
                text=f"Bit {bit}",
                variable=var,
                bg="white",
                activebackground="white",
                font=("Segoe UI", 9)
            ).pack(anchor="w", padx=35, pady=2)

        self.make_button(
            controls,
            "Reconstruct Image",
            self.reconstruct,
            "#16a34a"
        ).pack(fill="x", padx=15, pady=10)

        self.make_button(
            controls,
            "Save Result",
            self.save_result,
            "#334155"
        ).pack(fill="x", padx=15, pady=4)

        right = tk.Frame(main, bg="#eef2f7")
        right.pack(side="right", fill="both", expand=True)

        top = tk.Frame(right, bg="#eef2f7")
        top.pack(fill="both", expand=False)

        original_card = tk.Frame(
            top,
            bg="white",
            bd=1,
            relief="solid"
        )
        original_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 6)
        )

        tk.Label(
            original_card,
            text="ORIGINAL GRAYSCALE IMAGE",
            font=("Segoe UI", 11, "bold"),
            bg="white"
        ).pack(pady=7)

        self.original_label = tk.Label(
            original_card,
            text="Open an image",
            bg="#f8fafc",
            fg="#64748b"
        )
        self.original_label.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(0, 8)
        )

        result_card = tk.Frame(
            top,
            bg="white",
            bd=1,
            relief="solid"
        )
        result_card.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(6, 0)
        )

        self.result_title = tk.Label(
            result_card,
            text="RESULT",
            font=("Segoe UI", 11, "bold"),
            bg="white"
        )
        self.result_title.pack(pady=7)

        self.result_label = tk.Label(
            result_card,
            text="Select a bit plane\nor reconstruct an image",
            bg="#f8fafc",
            fg="#64748b"
        )
        self.result_label.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(0, 8)
        )

        planes_card = tk.Frame(
            right,
            bg="white",
            bd=1,
            relief="solid"
        )
        planes_card.pack(
            fill="both",
            expand=True,
            pady=(10, 0)
        )

        tk.Label(
            planes_card,
            text="8-BIT PLANES",
            font=("Segoe UI", 11, "bold"),
            bg="white"
        ).pack(pady=7)

        self.planes_frame = tk.Frame(
            planes_card,
            bg="white"
        )
        self.planes_frame.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=5
        )

        self.plane_labels = {}

        for index, bit in enumerate(range(7, -1, -1)):
            card = tk.Frame(
                self.planes_frame,
                bg="#f8fafc",
                bd=1,
                relief="solid"
            )

            row = index // 4
            column = index % 4

            card.grid(
                row=row,
                column=column,
                padx=4,
                pady=4,
                sticky="nsew"
            )

            self.planes_frame.grid_rowconfigure(
                row,
                weight=1
            )

            self.planes_frame.grid_columnconfigure(
                column,
                weight=1
            )

            tk.Label(
                card,
                text=f"BIT {bit}",
                font=("Segoe UI", 9, "bold"),
                bg="#f8fafc"
            ).pack(pady=3)

            label = tk.Label(
                card,
                text="—",
                bg="#e2e8f0"
            )

            label.pack(
                fill="both",
                expand=True,
                padx=4,
                pady=(0, 4)
            )

            self.plane_labels[bit] = label

        self.status = tk.Label(
            self.root,
            text="Ready — Open an image",
            bg="#1e293b",
            fg="white",
            anchor="w",
            padx=12,
            pady=5
        )
        self.status.pack(fill="x")

    def make_button(self, parent, text, command, color):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            pady=7
        )

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png *.bmp *.tif *.tiff"
                ),
                ("All Files", "*.*")
            ]
        )

        if not path:
            return

        image = cv2.imread(path)

        if image is None:
            messagebox.showerror(
                "Error",
                "Unable to open image."
            )
            return

        self.original = image

        self.gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        self.result = None
        self.clear_checks()

        self.display_original()
        self.generate_planes()

        self.result_label.config(
            image="",
            text="Select a bit plane\nor reconstruct an image"
        )

        self.result_title.config(
            text="RESULT"
        )

        self.status.config(
            text="Image loaded successfully"
        )

    def display_original(self):
        photo = self.make_photo(
            self.gray,
            400,
            230
        )

        self.original_photo = photo

        self.original_label.config(
            image=photo,
            text=""
        )

    def extract_plane(self, bit):
        plane = (self.gray >> bit) & 1
        return (plane * 255).astype(np.uint8)

    def generate_planes(self):
        for bit in range(8):
            plane = self.extract_plane(bit)

            photo = self.make_photo(
                plane,
                170,
                100
            )

            self.plane_photos[bit] = photo

            self.plane_labels[bit].config(
                image=photo,
                text=""
            )

    def show_plane(self, bit):
        if self.gray is None:
            return

        plane = self.extract_plane(bit)

        self.result = plane.copy()

        photo = self.make_photo(
            plane,
            400,
            230
        )

        self.result_photo = photo

        self.result_label.config(
            image=photo,
            text=""
        )

        self.result_title.config(
            text=f"BIT PLANE {bit}"
        )

        self.status.config(
            text=f"Displaying Bit Plane {bit}"
        )

    def reconstruct(self):
        if self.gray is None:
            messagebox.showwarning(
                "Warning",
                "Please open an image first."
            )
            return

        selected = [
            bit
            for bit in range(8)
            if self.check_vars[bit].get()
        ]

        if not selected:
            messagebox.showwarning(
                "No Bit Plane",
                "Select at least one bit plane."
            )
            return

        reconstructed = np.zeros_like(
            self.gray,
            dtype=np.uint8
        )

        for bit in selected:
            plane = (
                (self.gray >> bit) & 1
            ).astype(np.uint8)

            reconstructed |= (
                plane << bit
            )

        self.result = reconstructed

        photo = self.make_photo(
            reconstructed,
            400,
            230
        )

        self.result_photo = photo

        self.result_label.config(
            image=photo,
            text=""
        )

        bits = ", ".join(
            str(bit)
            for bit in sorted(
                selected,
                reverse=True
            )
        )

        self.result_title.config(
            text="RECONSTRUCTED IMAGE"
        )

        self.status.config(
            text=f"Reconstructed using Bit {bits}"
        )

    def make_photo(self, image, max_width, max_height):
        pil = Image.fromarray(image)

        width, height = pil.size

        scale = min(
            max_width / width,
            max_height / height,
            1
        )

        new_size = (
            max(1, int(width * scale)),
            max(1, int(height * scale))
        )

        pil = pil.resize(
            new_size,
            Image.Resampling.LANCZOS
        )

        return ImageTk.PhotoImage(pil)

    def save_result(self):
        if self.result is None:
            messagebox.showwarning(
                "No Result",
                "Select a bit plane or reconstruct an image first."
            )
            return

        path = filedialog.asksaveasfilename(
            title="Save Result",
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("BMP Image", "*.bmp"),
                ("JPEG Image", "*.jpg")
            ]
        )

        if not path:
            return

        if cv2.imwrite(path, self.result):
            messagebox.showinfo(
                "Success",
                "Result saved successfully."
            )
            self.status.config(
                text="Result saved successfully"
            )
        else:
            messagebox.showerror(
                "Error",
                "Unable to save result."
            )

    def clear_checks(self):
        for bit in range(8):
            self.check_vars[bit].set(False)

    def reset(self):
        self.original = None
        self.gray = None
        self.result = None

        self.original_label.config(
            image="",
            text="Open an image"
        )

        self.result_label.config(
            image="",
            text="Select a bit plane\nor reconstruct an image"
        )

        self.result_title.config(
            text="RESULT"
        )

        for bit in range(8):
            self.plane_labels[bit].config(
                image="",
                text="—"
            )

        self.clear_checks()

        self.status.config(
            text="Ready — Open an image"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = BitPlaneApp(root)
    root.mainloop()