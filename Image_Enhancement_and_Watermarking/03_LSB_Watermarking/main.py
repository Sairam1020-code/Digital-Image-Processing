import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont
import cv2
import numpy as np
import os


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Image Processing - LSB Watermarking")
        self.root.geometry("1450x900")
        self.root.minsize(1200, 750)
        self.root.configure(bg="#eef2f7")

        self.original_image = None
        self.watermarked_image = None
        self.original_path = None
        self.original_photo = None
        self.watermarked_photo = None

        self.watermark_color = "#ff0000"
        self.font_size = tk.IntVar(value=40)
        self.opacity = tk.IntVar(value=100)
        self.brightness = tk.IntVar(value=100)
        self.position = tk.StringVar(value="Bottom Right")
        self.show_box = tk.BooleanVar(value=False)

        self.create_header()
        self.create_ui()
        self.create_status()

    def create_header(self):
        header = tk.Frame(self.root, bg="#2563eb", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="LSB WATERMARKING",
            font=("Segoe UI", 25, "bold"),
            fg="white",
            bg="#2563eb"
        ).pack(pady=(12, 0))

        tk.Label(
            header,
            text="Digital Image Processing • Custom Color • Brightness • Position • LSB Bit 0",
            font=("Segoe UI", 10),
            fg="#dbeafe",
            bg="#2563eb"
        ).pack()

    def create_ui(self):
        main = tk.Frame(self.root, bg="#eef2f7")
        main.pack(fill="both", expand=True, padx=15, pady=15)

        left = tk.Frame(
            main,
            bg="white",
            width=340,
            bd=1,
            relief="solid"
        )
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)

        tk.Label(
            left,
            text="WATERMARK CONTROLS",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#172033"
        ).pack(pady=(15, 12))

        self.button(left, "📂  Open Image", self.open_image, "#2563eb").pack(
            fill="x", padx=20, pady=4
        )

        tk.Label(
            left,
            text="WATERMARK TEXT",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#475569"
        ).pack(anchor="w", padx=20, pady=(15, 4))

        self.text_entry = tk.Entry(
            left,
            font=("Segoe UI", 11),
            bd=1,
            relief="solid"
        )
        self.text_entry.pack(fill="x", padx=20, ipady=6)
        self.text_entry.insert(0, "IIIT NAGPUR")

        tk.Label(
            left,
            text="WATERMARK COLOR",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#475569"
        ).pack(anchor="w", padx=20, pady=(15, 4))

        color_frame = tk.Frame(left, bg="white")
        color_frame.pack(fill="x", padx=20)

        self.color_preview = tk.Label(
            color_frame,
            bg=self.watermark_color,
            width=5,
            height=1,
            relief="solid",
            bd=1
        )
        self.color_preview.pack(side="left")

        tk.Button(
            color_frame,
            text="🎨 Choose Color",
            command=self.choose_color,
            font=("Segoe UI", 9, "bold"),
            bg="#f1f5f9",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=5
        ).pack(side="left", padx=10)

        self.create_scale(left, "WATERMARK BRIGHTNESS", self.brightness, 0, 200)
        self.create_scale(left, "WATERMARK OPACITY", self.opacity, 10, 100)
        self.create_scale(left, "FONT SIZE", self.font_size, 15, 100)

        tk.Label(
            left,
            text="WATERMARK POSITION",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#475569"
        ).pack(anchor="w", padx=20, pady=(8, 4))

        positions = [
            "Top Left",
            "Top Center",
            "Top Right",
            "Center",
            "Bottom Left",
            "Bottom Center",
            "Bottom Right"
        ]

        self.position_menu = tk.OptionMenu(
            left,
            self.position,
            *positions,
            command=self.update_preview_if_possible
        )
        self.position_menu.config(
            font=("Segoe UI", 9),
            bg="#f8fafc",
            relief="solid",
            bd=1
        )
        self.position_menu.pack(fill="x", padx=20)

        tk.Checkbutton(
            left,
            text="Add watermark background box",
            variable=self.show_box,
            command=self.update_preview_if_possible,
            bg="white",
            font=("Segoe UI", 9),
            activebackground="white"
        ).pack(anchor="w", padx=20, pady=8)

        self.button(
            left,
            "👁  Preview Watermark",
            self.preview_watermark,
            "#7c3aed"
        ).pack(fill="x", padx=20, pady=4)

        self.button(
            left,
            "🔐  Embed in LSB",
            self.embed_lsb,
            "#16a34a"
        ).pack(fill="x", padx=20, pady=4)

        self.button(
            left,
            "🔓  Extract Watermark",
            self.extract_lsb,
            "#1d4ed8"
        ).pack(fill="x", padx=20, pady=4)

        self.button(
            left,
            "💾  Save Watermarked Image",
            self.save_image,
            "#475569"
        ).pack(fill="x", padx=20, pady=4)

        self.button(
            left,
            "↻  Reset",
            self.reset,
            "#64748b"
        ).pack(fill="x", padx=20, pady=4)

        tk.Label(
            left,
            text="EXTRACTED WATERMARK",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#475569"
        ).pack(anchor="w", padx=20, pady=(12, 4))

        self.extracted_box = tk.Text(
            left,
            height=4,
            font=("Segoe UI", 9),
            wrap="word",
            bd=1,
            relief="solid"
        )
        self.extracted_box.pack(fill="x", padx=20)

        right = tk.Frame(main, bg="#eef2f7")
        right.pack(side="right", fill="both", expand=True)

        image_area = tk.Frame(right, bg="#eef2f7")
        image_area.pack(fill="both", expand=True)

        original_card = tk.Frame(
            image_area,
            bg="white",
            bd=1,
            relief="solid"
        )
        original_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )

        tk.Label(
            original_card,
            text="ORIGINAL IMAGE",
            font=("Segoe UI", 12, "bold"),
            bg="white"
        ).pack(pady=8)

        self.original_label = tk.Label(
            original_card,
            text="Open an image",
            bg="#f8fafc",
            fg="#64748b"
        )
        self.original_label.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        watermark_card = tk.Frame(
            image_area,
            bg="white",
            bd=1,
            relief="solid"
        )
        watermark_card.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(7, 0)
        )

        tk.Label(
            watermark_card,
            text="WATERMARKED IMAGE",
            font=("Segoe UI", 12, "bold"),
            bg="white"
        ).pack(pady=8)

        self.watermarked_label = tk.Label(
            watermark_card,
            text="Watermarked image will appear here",
            bg="#f8fafc",
            fg="#64748b"
        )
        self.watermarked_label.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        info_card = tk.Frame(
            right,
            bg="white",
            bd=1,
            relief="solid",
            height=150
        )
        info_card.pack(fill="x", pady=(15, 0))
        info_card.pack_propagate(False)

        tk.Label(
            info_card,
            text="WATERMARK SETTINGS",
            font=("Segoe UI", 12, "bold"),
            bg="white"
        ).pack(pady=(10, 3))

        self.settings_label = tk.Label(
            info_card,
            text="Color: Red     Brightness: 100%     Opacity: 100%     Position: Bottom Right",
            font=("Segoe UI", 10),
            bg="white",
            fg="#475569"
        )
        self.settings_label.pack(pady=5)

        self.lsb_label = tk.Label(
            info_card,
            text="LSB: Not embedded",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fafc",
            fg="#475569",
            padx=10,
            pady=6
        )
        self.lsb_label.pack(padx=30, fill="x")

    def create_scale(self, parent, title, variable, minimum, maximum):
        tk.Label(
            parent,
            text=title,
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#475569"
        ).pack(anchor="w", padx=20, pady=(15, 2))

        scale = tk.Scale(
            parent,
            from_=minimum,
            to=maximum,
            orient="horizontal",
            variable=variable,
            bg="white",
            highlightthickness=0,
            troughcolor="#dbeafe",
            command=self.update_preview_if_possible
        )
        scale.pack(fill="x", padx=20)

    def button(self, parent, text, command, color):
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

    def create_status(self):
        self.status = tk.Label(
            self.root,
            text="Ready — Open an image",
            bg="#1e293b",
            fg="white",
            anchor="w",
            padx=15,
            pady=6
        )
        self.status.pack(fill="x")

    def choose_color(self):
        color = colorchooser.askcolor(
            title="Choose Watermark Color",
            initialcolor=self.watermark_color
        )

        if color[1]:
            self.watermark_color = color[1]
            self.color_preview.config(bg=self.watermark_color)
            self.update_settings_text()
            self.update_preview_if_possible()

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"),
                ("All Files", "*.*")
            ]
        )

        if not path:
            return

        image = cv2.imread(path, cv2.IMREAD_COLOR)

        if image is None:
            messagebox.showerror("Error", "Unable to open image.")
            return

        self.original_image = image
        self.original_path = path
        self.watermarked_image = None

        self.display_original()

        self.watermarked_label.config(
            image="",
            text="Watermarked image will appear here"
        )

        self.update_capacity()

        self.status.config(text="Image loaded successfully")
        self.lsb_label.config(text="LSB: Not embedded")

    def preview_watermark(self):
        if self.original_image is None:
            messagebox.showwarning(
                "No Image",
                "Please open an image first."
            )
            return

        result = self.create_visible_watermark(
            self.original_image
        )

        self.watermarked_image = result
        self.display_watermarked()

        self.lsb_label.config(
            text="Preview only — LSB watermark not embedded"
        )

        self.status.config(
            text="Visible watermark preview generated"
        )

    def create_visible_watermark(self, image):
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        base = Image.fromarray(rgb).convert("RGBA")

        overlay = Image.new(
            "RGBA",
            base.size,
            (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(overlay)

        text = self.text_entry.get() or "WATERMARK"
        font = self.get_font(self.font_size.get())
        color = self.hex_to_rgb(self.watermark_color)

        brightness_factor = self.brightness.get() / 100.0

        r = int(min(255, color[0] * brightness_factor))
        g = int(min(255, color[1] * brightness_factor))
        b = int(min(255, color[2] * brightness_factor))

        alpha = int(255 * self.opacity.get() / 100)

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        width, height = base.size
        margin = max(20, int(min(width, height) * 0.03))
        position = self.position.get()

        if position == "Top Left":
            x, y = margin, margin
        elif position == "Top Center":
            x, y = (width - text_width) // 2, margin
        elif position == "Top Right":
            x, y = width - text_width - margin, margin
        elif position == "Center":
            x = (width - text_width) // 2
            y = (height - text_height) // 2
        elif position == "Bottom Left":
            x, y = margin, height - text_height - margin
        elif position == "Bottom Center":
            x = (width - text_width) // 2
            y = height - text_height - margin
        else:
            x = width - text_width - margin
            y = height - text_height - margin

        if self.show_box.get():
            padding = 10
            box = (
                x - padding,
                y - padding,
                x + text_width + padding,
                y + text_height + padding
            )

            draw.rounded_rectangle(
                box,
                radius=8,
                fill=(0, 0, 0, 130)
            )

        draw.text(
            (x, y),
            text,
            font=font,
            fill=(r, g, b, alpha)
        )

        result = Image.alpha_composite(base, overlay)
        result = np.array(result.convert("RGB"))

        return cv2.cvtColor(
            result,
            cv2.COLOR_RGB2BGR
        )

    def get_font(self, size):
        fonts = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/calibrib.ttf"
        ]

        for path in fonts:
            if os.path.exists(path):
                return ImageFont.truetype(path, size)

        return ImageFont.load_default()

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(
            int(hex_color[i:i + 2], 16)
            for i in (0, 2, 4)
        )

    def embed_lsb(self):
        if self.original_image is None:
            messagebox.showwarning(
                "No Image",
                "Please open an image first."
            )
            return

        text = self.text_entry.get()

        if not text:
            messagebox.showwarning(
                "Empty Watermark",
                "Enter watermark text."
            )
            return

        data = text.encode("utf-8")
        data_length = len(data)

        height, width = self.original_image.shape[:2]
        total_bits = height * width
        required_bits = 32 + data_length * 8

        if required_bits > total_bits:
            maximum = (total_bits - 32) // 8

            messagebox.showerror(
                "Watermark Too Large",
                f"Watermark size: {data_length} bytes\n"
                f"Maximum allowed: {maximum} bytes"
            )
            return

        visible = self.create_visible_watermark(
            self.original_image
        )

        result = visible.copy()
        blue = result[:, :, 0]
        flat = blue.flatten()

        length_array = np.array([data_length], dtype=">u4")
        length_bits = np.unpackbits(
            length_array.view(np.uint8)
        )

        message_array = np.frombuffer(
            data,
            dtype=np.uint8
        )

        message_bits = np.unpackbits(message_array)

        payload = np.concatenate(
            (length_bits, message_bits)
        )

        flat[:len(payload)] = (
            flat[:len(payload)] & 0xFE
        ) | payload

        result[:, :, 0] = flat.reshape(height, width)

        self.watermarked_image = result
        self.display_watermarked()
        self.update_settings_text()

        self.lsb_label.config(
            text="LSB: WATERMARK EMBEDDED\nBit 0 • Blue channel"
        )

        self.status.config(
            text="Watermark embedded successfully into LSB Bit 0"
        )

        messagebox.showinfo(
            "Success",
            f"Watermark embedded successfully!\n\n"
            f"Text: {text}\n"
            f"Color: {self.watermark_color}\n"
            f"Brightness: {self.brightness.get()}%\n"
            f"Opacity: {self.opacity.get()}%\n"
            f"Position: {self.position.get()}\n\n"
            f"Hidden data: Bit 0 (LSB)"
        )

    def extract_lsb(self):
        if self.watermarked_image is None:
            messagebox.showwarning(
                "No Watermarked Image",
                "Please embed a watermark first."
            )
            return

        blue = self.watermarked_image[:, :, 0]
        flat = blue.flatten()

        header_bits = (
            flat[:32] & 1
        ).astype(np.uint8)

        header_bytes = np.packbits(
            header_bits
        ).tobytes()

        if len(header_bytes) != 4:
            messagebox.showerror(
                "Error",
                "Invalid watermark header."
            )
            return

        data_length = int.from_bytes(
            header_bytes,
            byteorder="big"
        )

        available = len(flat) - 32
        required = data_length * 8

        if data_length <= 0:
            messagebox.showerror(
                "No Watermark",
                "No valid watermark was found."
            )
            return

        if required > available:
            messagebox.showerror(
                "Invalid Watermark",
                "The watermark data is invalid."
            )
            return

        bits = (
            flat[32:32 + required] & 1
        ).astype(np.uint8)

        data = np.packbits(bits).tobytes()

        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            messagebox.showerror(
                "Invalid Watermark",
                "The selected image does not contain a valid text watermark."
            )
            return

        self.extracted_box.delete("1.0", tk.END)
        self.extracted_box.insert(tk.END, text)

        self.status.config(
            text="Watermark extracted successfully"
        )

        messagebox.showinfo(
            "Watermark Extracted",
            f"Hidden watermark:\n\n{text}"
        )

    def save_image(self):
        if self.watermarked_image is None:
            messagebox.showwarning(
                "No Result",
                "Please create a watermark first."
            )
            return

        path = filedialog.asksaveasfilename(
            title="Save Watermarked Image",
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("BMP Image", "*.bmp"),
                ("TIFF Image", "*.tif")
            ]
        )

        if not path:
            return

        success = cv2.imwrite(
            path,
            self.watermarked_image
        )

        if success:
            messagebox.showinfo(
                "Saved",
                "Image saved successfully.\n\n"
                "PNG/BMP/TIFF is recommended because JPEG "
                "compression can destroy LSB data."
            )
            self.status.config(
                text="Watermarked image saved"
            )
        else:
            messagebox.showerror(
                "Error",
                "Unable to save image."
            )

    def update_settings_text(self):
        self.settings_label.config(
            text=(
                f"Color: {self.watermark_color}     "
                f"Brightness: {self.brightness.get()}%     "
                f"Opacity: {self.opacity.get()}%     "
                f"Position: {self.position.get()}"
            )
        )

    def update_preview_if_possible(self, event=None):
        self.update_settings_text()

        if self.original_image is not None:
            self.preview_watermark()

    def display_original(self):
        rgb = cv2.cvtColor(
            self.original_image,
            cv2.COLOR_BGR2RGB
        )

        photo = self.make_photo(rgb, 520, 430)
        self.original_photo = photo

        self.original_label.config(
            image=photo,
            text=""
        )

    def display_watermarked(self):
        rgb = cv2.cvtColor(
            self.watermarked_image,
            cv2.COLOR_BGR2RGB
        )

        photo = self.make_photo(rgb, 520, 430)
        self.watermarked_photo = photo

        self.watermarked_label.config(
            image=photo,
            text=""
        )

    def make_photo(self, image, max_width, max_height):
        pil = Image.fromarray(image)
        width, height = pil.size

        scale = min(
            max_width / width,
            max_height / height
        )

        new_width = max(1, int(width * scale))
        new_height = max(1, int(height * scale))

        pil = pil.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )

        return ImageTk.PhotoImage(pil)

    def update_capacity(self):
        if self.original_image is None:
            return

        height, width = self.original_image.shape[:2]
        total_bits = height * width
        max_bytes = (total_bits - 32) // 8

        self.status.config(
            text=f"Image loaded • LSB capacity: {max_bytes:,} bytes"
        )

    def reset(self):
        self.original_image = None
        self.watermarked_image = None
        self.original_path = None

        self.original_label.config(
            image="",
            text="Open an image"
        )

        self.watermarked_label.config(
            image="",
            text="Watermarked image will appear here"
        )

        self.extracted_box.delete("1.0", tk.END)

        self.text_entry.delete(0, tk.END)
        self.text_entry.insert(0, "IIIT NAGPUR")

        self.brightness.set(100)
        self.opacity.set(100)
        self.font_size.set(40)
        self.position.set("Bottom Right")

        self.watermark_color = "#ff0000"
        self.color_preview.config(bg="#ff0000")

        self.lsb_label.config(text="LSB: Not embedded")

        self.settings_label.config(
            text=(
                "Color: #ff0000     "
                "Brightness: 100%     "
                "Opacity: 100%     "
                "Position: Bottom Right"
            )
        )

        self.status.config(
            text="Reset completed — Open an image"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()