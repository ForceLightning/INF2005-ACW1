import os
import sys

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
from moviepy.editor import VideoFileClip
import threading

def main():
    pygame.mixer.init()
    pygame.font.init()

    root = Tk()
    root.title("Steganography")
    root.geometry("500x500")
    root.resizable(False, False)

    open_button = Button(root, text="Open File", command=lambda: open_file_dialog(root))
    open_button.pack()

    root.mainloop()

def open_file_dialog(root):
    file_path = filedialog.askopenfilename()
    if file_path:
        file_extension = file_path.split('.')[-1].lower()
        if file_extension in ('jpg', 'jpeg', 'png', 'gif'):
            # Preview Image
            image = Image.open(file_path)
            image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(image)
            img_label = Label(root, image=photo)
            img_label.photo = photo
            img_label.pack()
        elif file_extension in ('mp3', 'wav'):
            # Play Audio
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
        elif file_extension in ('mp4', 'avi', 'mov'):
            # Play Video
            video_thread = threading.Thread(target=play_video, args=(root, file_path))
            video_thread.start()
        else:
            messagebox.showinfo("Unsupported Format", "Unsupported file format for preview.")

def play_video(root, file_path):
    try:
        video_clip = VideoFileClip(file_path)
        video_clip.preview(fps=24, audio=True, threaded=True, winname="Video Preview")
    except Exception as e:
        messagebox.showerror("Error", f"Error playing video: {str(e)}")

if __name__ == "__main__":
    main()
