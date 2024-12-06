import tkinter as tk
from PIL import Image, ImageTk
import ctypes


def set_dpi_awareness():
    """Set the DPI awareness to ensure correct scaling on high-DPI displays."""
    ctypes.windll.shcore.SetProcessDpiAwareness(1)


def load_image(image_path, size=None): #Load and resize an image.
    image = Image.open(image_path)
    if size:
        image = image.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)


def create_button(window, image, command, x, y, width=None, height=None): #Create a button with an image, placed at the specified coordinates.
    if width and height:
        image = image.resize((width, height), Image.Resampling.LANCZOS)
    button = tk.Button(window, image=image, bg="#ffe6e6", bd=0, highlightthickness=0, relief="flat", activebackground="#ffe6e6", command=command)
    window.canvas.create_window(x, y, window=button, anchor="center")
    return button


def open_settings(root):
    set_dpi_awareness()  # Ensure DPI scaling is correct

    # Create a new settings window
    setting_window = tk.Toplevel(root)
    setting_window.title("Cài đặt")

    # Set window size and disable resizing
    width, height = 1920, 1080
    setting_window.geometry(f"{width}x{height}")
    setting_window.resizable(False, False)

    # Create a Canvas for the background
    setting_window.canvas = tk.Canvas(setting_window, width=width, height=height)
    setting_window.canvas.pack()

    # Load background image and display it
    background_image = load_image("source\setting_background.png", size=(width, height))
    setting_window.canvas.create_image(0, 0, image=background_image, anchor="nw")
    setting_window.background_image = background_image  # Prevent garbage collection

    # Load and display logo image
    logo_image = load_image("source\\name_icon.png", size=(192 * 2, 108 * 2))
    setting_window.canvas.create_image(width // 4, 260, image=logo_image, anchor="n")
    setting_window.logo_image = logo_image  # Prevent garbage collection

    # Create resume button
    resume_image = load_image("source\\resume_icon.png", size=(60 * 5, 30 * 5))
    resume_button = create_button(setting_window, resume_image, setting_window.destroy, width // 2, int(height * 0.65))

    # Create restart button
    restart_image = load_image("source\\restart_icon.jpg", size=(60 * 5, 40 * 5))
    create_button(setting_window, restart_image, lambda: print("Restarting..."), width // 2, int(height * 0.45))

    # Create quit button
    quit_image = load_image("source\quite_icon.png", size=(60 * 5, 30 * 5))
    create_button(setting_window, quit_image, setting_window.quit, width // 2, int(height * 0.8))

    # Prevent garbage collection of images
    setting_window.resume_image = resume_image
    setting_window.restart_image = restart_image
    setting_window.quit_image = quit_image

