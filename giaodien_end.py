import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import sys
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

def open_home():
    root.destroy()
    subprocess.run([sys.executable, 'giaodien_open.py'])

root = tk.Tk()
root.title("Game Python")
width, height = 1920, 1080
root.geometry(f"{width}x{height}")
root.resizable(False, False)

background_image = Image.open("source\end_background.jpg")
background_image = background_image.resize((width, height), Image.Resampling.LANCZOS)
background_tk = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()
canvas.create_image(0, 0, image=background_tk, anchor="nw")

play_image2 = Image.open("source\home_icon.png")
play_image2 = play_image2.resize((150, 150), Image.Resampling.LANCZOS)
play_tk2 = ImageTk.PhotoImage(play_image2)

play_button2 = tk.Button(root, image=play_tk2, bg="#ffffff", bd=0, highlightthickness=0, relief="flat",
                         activebackground="#ffffff", command=open_home)
play_button2.place(relx=0.95, rely=0.07, anchor="center")

root.mainloop()
