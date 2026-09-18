import json
import struct
from collections import Counter
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import numpy as np
from PIL import Image, ImageTk


MAGIC = b"SFC1"


class ShannonFanoApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Shannon-Fano Image Compression")
        self.root.geometry("1050x700")
        self.root.minsize(950, 650)

        self.image_path = None
        self.preview_image = None

        self.setup_style()
        self.create_widgets()

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 22, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Section.TLabel",
            font=("Segoe UI", 12, "bold")
        )

        style.configure(
            "Action.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 8)
        )

    def create_widgets(self):

        header = ttk.Frame(self.root, padding=20)
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Shannon-Fano Image Compression",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="Lossless entropy-based image compression",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(3, 0))

        main = ttk.Frame(self.root, padding=(20, 0, 20, 20))
        main.pack(fill="both", expand=True)

        left = ttk.LabelFrame(
            main,
            text="Image",
            padding=15
        )
        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        right = ttk.LabelFrame(
            main,
            text="Compression Details",
            padding=15
        )
        right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        self.preview_label = ttk.Label(
            left,
            text="No image selected",
            anchor="center"
        )
        self.preview_label.pack(
            fill="both",
            expand=True,
            pady=10
        )

        self.file_label = ttk.Label(
            left,
            text="",
            wraplength=400
        )
        self.file_label.pack(
            fill="x",
            pady=5
        )

        buttons = ttk.Frame(left)
        buttons.pack(fill="x", pady=(10, 0))

        ttk.Button(
            buttons,
            text="Select Image",
            command=self.select_image,
            style="Action.TButton"
        ).pack(
            side="left",
            expand=True,
            padx=(0, 5)
        )

        ttk.Button(
            buttons,
            text="Compress",
            command=self.compress,
            style="Action.TButton"
        ).pack(
            side="left",
            expand=True,
            padx=5
        )

        ttk.Button(
            buttons,
            text="Decompress",
            command=self.decompress,
            style="Action.TButton"
        ).pack(
            side="left",
            expand=True,
            padx=(5, 0)
        )

        stats_frame = ttk.LabelFrame(
            right,
            text="Statistics",
            padding=10
        )
        stats_frame.pack(fill="x")

        self.stats_text = tk.Text(
            stats_frame,
            height=9,
            font=("Consolas", 10),
            relief="flat",
            bg="#f5f5f5"
        )
        self.stats_text.pack(fill="x")
        self.stats_text.config(state="disabled")

        code_frame = ttk.LabelFrame(
            right,
            text="Shannon-Fano Codes",
            padding=10
        )
        code_frame.pack(
            fill="both",
            expand=True,
            pady=(12, 0)
        )

        columns = (
            "symbol",
            "frequency",
            "probability",
            "code"
        )

        self.code_table = ttk.Treeview(
            code_frame,
            columns=columns,
            show="headings"
        )

        self.code_table.heading(
            "symbol",
            text="Pixel"
        )
        self.code_table.heading(
            "frequency",
            text="Frequency"
        )
        self.code_table.heading(
            "probability",
            text="Probability"
        )
        self.code_table.heading(
            "code",
            text="Code"
        )

        self.code_table.column(
            "symbol",
            width=70,
            anchor="center"
        )
        self.code_table.column(
            "frequency",
            width=90,
            anchor="center"
        )
        self.code_table.column(
            "probability",
            width=100,
            anchor="center"
        )
        self.code_table.column(
            "code",
            width=150,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            code_frame,
            orient="vertical",
            command=self.code_table.yview
        )

        self.code_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.code_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.status_var = tk.StringVar(
            value="Ready"
        )

        status = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            padding=8
        )
        status.pack(
            fill="x",
            side="bottom"
        )

    def select_image(self):

        path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                (
                    "Image Files",
                    "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"
                )
            ]
        )

        if not path:
            return

        self.image_path = path

        self.show_preview(path)

        self.file_label.config(
            text=f"Selected:\n{Path(path).name}"
        )

        self.status_var.set(
            "Image selected successfully."
        )

    def show_preview(self, path):

        image = Image.open(path).convert("L")

        image.thumbnail((420, 420))

        self.preview_image = ImageTk.PhotoImage(
            image
        )

        self.preview_label.config(
            image=self.preview_image,
            text=""
        )

    def update_stats(self, text):

        self.stats_text.config(state="normal")
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert("1.0", text)
        self.stats_text.config(state="disabled")

    def clear_table(self):

        for item in self.code_table.get_children():
            self.code_table.delete(item)

    def display_codes(
        self,
        frequencies,
        codes
    ):

        self.clear_table()

        total = sum(frequencies.values())

        for symbol, frequency in sorted(
            frequencies.items(),
            key=lambda x: (-x[1], x[0])
        ):

            probability = frequency / total

            self.code_table.insert(
                "",
                "end",
                values=(
                    symbol,
                    frequency,
                    f"{probability:.5f}",
                    codes[symbol]
                )
            )

    @staticmethod
    def build_codes(frequencies):

        items = sorted(
            frequencies.items(),
            key=lambda x: (-x[1], x[0])
        )

        codes = {
            symbol: ""
            for symbol, _ in items
        }

        if len(items) == 1:
            codes[items[0][0]] = "0"
            return codes

        def split(group):

            if len(group) <= 1:
                return

            total = sum(
                frequency
                for _, frequency in group
            )

            left_sum = 0
            best_index = 1
            best_difference = float("inf")

            for i in range(1, len(group)):

                left_sum += group[i - 1][1]

                difference = abs(
                    total - 2 * left_sum
                )

                if difference < best_difference:
                    best_difference = difference
                    best_index = i

            left = group[:best_index]
            right = group[best_index:]

            for symbol, _ in left:
                codes[symbol] += "0"

            for symbol, _ in right:
                codes[symbol] += "1"

            split(left)
            split(right)

        split(items)

        return codes

    @staticmethod
    def pack_bits(bits):

        padding = (
            8 - len(bits) % 8
        ) % 8

        padded = bits + "0" * padding

        data = bytearray()

        for i in range(
            0,
            len(padded),
            8
        ):
            data.append(
                int(
                    padded[i:i + 8],
                    2
                )
            )

        return bytes(data), padding

    @staticmethod
    def unpack_bits(data, padding):

        bits = "".join(
            f"{byte:08b}"
            for byte in data
        )

        if padding:
            bits = bits[:-padding]

        return bits

    def compress(self):

        if not self.image_path:
            messagebox.showwarning(
                "No Image",
                "Please select an image first."
            )
            return

        output_path = filedialog.asksaveasfilename(
            title="Save Shannon-Fano File",
            defaultextension=".sfc",
            filetypes=[
                (
                    "Shannon-Fano File",
                    "*.sfc"
                )
            ]
        )

        if not output_path:
            return

        try:

            image = Image.open(
                self.image_path
            ).convert("L")

            array = np.array(
                image,
                dtype=np.uint8
            )

            pixels = array.flatten()

            frequencies = Counter(
                int(pixel)
                for pixel in pixels
            )

            codes = self.build_codes(
                frequencies
            )

            encoded_bits = "".join(
                codes[int(pixel)]
                for pixel in pixels
            )

            compressed_data, padding = (
                self.pack_bits(encoded_bits)
            )

            header = {
                "width": image.width,
                "height": image.height,
                "mode": "L",
                "codes": {
                    str(symbol): code
                    for symbol, code
                    in codes.items()
                },
                "padding": padding,
                "encoded_bits": len(encoded_bits)
            }

            header_data = json.dumps(
                header,
                separators=(",", ":")
            ).encode("utf-8")

            with open(
                output_path,
                "wb"
            ) as file:

                file.write(MAGIC)

                file.write(
                    struct.pack(
                        ">I",
                        len(header_data)
                    )
                )

                file.write(header_data)
                file.write(compressed_data)

            original_size = len(pixels)
            compressed_size = Path(
                output_path
            ).stat().st_size

            ratio = (
                original_size /
                compressed_size
            )

            saved = (
                1 -
                compressed_size /
                original_size
            ) * 100

            self.display_codes(
                frequencies,
                codes
            )

            self.update_stats(
                f"Image Size          : "
                f"{image.width} × {image.height}\n\n"
                f"Original Size       : "
                f"{original_size:,} bytes\n"
                f"Compressed Size     : "
                f"{compressed_size:,} bytes\n"
                f"Encoded Bits        : "
                f"{len(encoded_bits):,}\n"
                f"Unique Gray Levels  : "
                f"{len(frequencies)}\n\n"
                f"Compression Ratio   : "
                f"{ratio:.3f}:1\n"
                f"Space Saved         : "
                f"{saved:.2f}%"
            )

            self.status_var.set(
                "Shannon-Fano compression completed."
            )

            messagebox.showinfo(
                "Compression Complete",
                "Image compressed successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Compression Error",
                str(error)
            )

    def decompress(self):

        input_path = filedialog.askopenfilename(
            title="Open Shannon-Fano File",
            filetypes=[
                (
                    "Shannon-Fano File",
                    "*.sfc"
                )
            ]
        )

        if not input_path:
            return

        output_path = filedialog.asksaveasfilename(
            title="Save Decompressed Image",
            defaultextension=".png",
            filetypes=[
                (
                    "PNG Image",
                    "*.png"
                ),
                (
                    "BMP Image",
                    "*.bmp"
                ),
                (
                    "TIFF Image",
                    "*.tiff"
                )
            ]
        )

        if not output_path:
            return

        try:

            with open(
                input_path,
                "rb"
            ) as file:

                magic = file.read(4)

                if magic != MAGIC:
                    raise ValueError(
                        "Invalid Shannon-Fano file."
                    )

                header_length = struct.unpack(
                    ">I",
                    file.read(4)
                )[0]

                header = json.loads(
                    file.read(
                        header_length
                    ).decode("utf-8")
                )

                compressed_data = file.read()

            reverse_codes = {
                code: int(symbol)
                for symbol, code
                in header["codes"].items()
            }

            bits = self.unpack_bits(
                compressed_data,
                header["padding"]
            )

            pixels = []
            current_code = ""

            for bit in bits:

                current_code += bit

                if current_code in reverse_codes:

                    pixels.append(
                        reverse_codes[current_code]
                    )

                    current_code = ""

            expected = (
                header["width"] *
                header["height"]
            )

            if len(pixels) != expected:
                raise ValueError(
                    "Decoded pixel count is incorrect."
                )

            array = np.array(
                pixels,
                dtype=np.uint8
            ).reshape(
                header["height"],
                header["width"]
            )

            image = Image.fromarray(
                array,
                mode="L"
            )

            image.save(output_path)

            self.show_preview(
                output_path
            )

            self.file_label.config(
                text=f"Decompressed:\n"
                     f"{Path(output_path).name}"
            )

            self.status_var.set(
                "Shannon-Fano decompression completed."
            )

            messagebox.showinfo(
                "Decompression Complete",
                "Image reconstructed successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Decompression Error",
                str(error)
            )


if __name__ == "__main__":

    root = tk.Tk()

    app = ShannonFanoApp(root)

    root.mainloop()