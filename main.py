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

from steganography.decoder import ImageDecoder, AudioDecoder, VideoDecoder
from steganography.encoder import ImageEncoder, AudioEncoder, VideoEncoder

# Initialize Steganography and Decoders
# stega = Steganography()
image_decoder = ImageDecoder()
audio_decoder = AudioDecoder()
video_decoder = VideoDecoder()
image_encoder = ImageEncoder()
audio_encoder = AudioEncoder()
video_encoder = VideoEncoder()

def main():
    pygame.mixer.init()
    pygame.font.init()

    root = Tk()
    root.title("Steganography")
    root.geometry("800x500")
    root.resizable(False, False)

    # Create a frame to hold the before and after images
    frame = Frame(root)
    frame.pack()

    # Create Labels for before and after images
    before_image_label = Label(frame, text="Before Image")
    before_image_label.grid(row=0, column=0, padx=10, pady=10)
    before_image = Label(frame)
    before_image.grid(row=1, column=0, padx=10, pady=10)

    after_image_label = Label(frame, text="After Image")
    after_image_label.grid(row=0, column=1, padx=10, pady=10)
    after_image = Label(frame)
    after_image.grid(row=1, column=1, padx=10, pady=10)

    # TODO: Add and initialize widgets here

    secret_message_label = Label(root, text="Enter Secret Message:")
    secret_message_label.pack()
    secret_message_entry = Entry(root, width=50)
    secret_message_entry.pack()

    def browse_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            file_extension = file_path.split('.')[-1].lower()
            if file_extension in ('jpg', 'jpeg', 'png', 'gif'):
                # Display Before Image
                display_image(before_image, file_path)
                # Encode and Display After Image
                secret_message = secret_message_entry.get()
                encoded_image_path = encode_image(file_path, secret_message)
                display_image(after_image, encoded_image_path)
            elif file_extension in ('mp3', 'wav'):
                # Play Audio
                play_audio(file_path)
            elif file_extension in ('mp4', 'avi', 'mov'):
                # Play Video
                play_video(root, file_path)
            else:
                messagebox.showinfo("Unsupported Format", "Unsupported file format for preview.")

    browse_button = Button(root, text="Browse Files", command=browse_file)
    browse_button.pack()

    root.mainloop()

def display_image(label, file_path):
    image = Image.open(file_path)
    # Limit the size of the displayed image
    image.thumbnail((200, 200))
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.photo = photo

def encode_image(file_path, secret_message):
    # Encode the secret message into the image and save it as a new file
    encoded_image_path = file_path.replace(".", "_encoded.")
    image_encoder.encode(file_path, secret_message, encoded_image_path)
    return encoded_image_path

def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def play_video(root, file_path):
    video_thread = threading.Thread(target=play_video_clip, args=(root, file_path))
    video_thread.start()

def play_video_clip(root, file_path):
    try:
        video_clip = VideoFileClip(file_path)
        video_clip.preview(fps=24, audio=True, threaded=True, winname="Video Preview")
    except Exception as e:
        messagebox.showerror("Error", f"Error playing video: {str(e)}")

if __name__ == "__main__":
    main()
