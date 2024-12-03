import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import numpy as np
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Курбонзода Зухал")
        self.pack()
        self.create_widgets()
        self.transformations = []
        self.original_image = None
        self.transformed_image = None

    def create_widgets(self):
        button_width = 24

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side="top", fill="x", padx=10, pady=10)

        self.open_button = tk.Button(self.top_frame, text="Открыть", width=button_width, command=self.load_image)
        self.open_button.pack(side="left", padx=10, pady=5)

        self.affine_button = tk.Button(self.top_frame, text="Афинные преобразования", width=button_width, command=self.apply_affine_transformation)
        self.affine_button.pack(side="left", padx=10, pady=5)

        self.nonlinear_button = tk.Button(self.top_frame, text="Нелинейные преобразования", width=button_width, command=self.apply_nonlinear_transformation)
        self.nonlinear_button.pack(side="left", padx=10, pady=5)

        self.save_button = tk.Button(self.top_frame, text="Сохранить", width=button_width, command=self.save_result)
        self.save_button.pack(side="left", padx=10, pady=5)

        self.restore_button = tk.Button(self.top_frame, text="Восстановить", width=button_width, command=self.restore_original)
        self.restore_button.pack(side="left", padx=10, pady=5)

        self.image_frame = tk.Frame(self)
        self.image_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill="both", expand=True)

    def load_image(self):
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if image_path:
            self.original_image = Image.open(image_path)
            self.transformed_image = self.original_image.copy()
            self.update_display_image(self.transformed_image)

    def apply_affine_transformation(self):
        if self.transformed_image:
            self.transformed_image = self.transformed_image.transpose(Image.FLIP_LEFT_RIGHT)
            angle = 30
            self.transformed_image = self.transformed_image.rotate(angle)
            self.update_display_image(self.transformed_image)

    def apply_nonlinear_transformation(self):
        if self.transformed_image:
            pixel_array = np.array(self.transformed_image)
            width, height = pixel_array.shape[1], pixel_array.shape[0]
            transformed_array = np.zeros_like(pixel_array)

            for i in range(height):
                for j in range(width):
                    x_prime = i * j
                    y_prime = j
                    if 0 <= x_prime < height and 0 <= y_prime < width:
                        transformed_array[i, j] = pixel_array[x_prime % height, y_prime]

            self.transformed_image = Image.fromarray(transformed_array)
            self.update_display_image(self.transformed_image)

    def save_result(self):
        if self.transformed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                self.transformed_image.save(file_path)

    def restore_original(self):
        if self.original_image:
            self.transformed_image = self.original_image.copy()
            self.update_display_image(self.transformed_image)

    def update_display_image(self, img):
        img.thumbnail((800, 400))
        self.displayed_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.displayed_image)
        self.image_label.image = self.displayed_image

root = tk.Tk()
app = Application(master=root)
app.mainloop()