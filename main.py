import os
import sys
import threading

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pygame
from moviepy.editor import VideoFileClip
from tkinterdnd2 import TkinterDnD, DND_FILES

from steganography.steganography import Steganography
from steganography.util import IMAGE_EXTENSIONS, AUDIO_EXTENSIONS, VIDEO_EXTENSIONS

# Initialize Steganography and Decoders
stega = Steganography()

# Function to handle drop event
def drop(event):
    file_path = event.data
    print(f"File Path: {file_path}") # For debug
    process_file(file_path, is_dropped=True)

def display_image(label, file_path):
    image = Image.open(file_path)
    # Limit the size of the displayed image
    image.thumbnail((200, 200))
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.photo = photo

def process_file(file_path, is_dropped=False):
    if file_path:
        file_extension = file_path.split('.')[-1].lower()
        print(f"File Extension: {file_extension}")
        if file_extension in IMAGE_EXTENSIONS:
            if not is_dropped:
                # Display Before Image
                display_image(before_image, file_path)
                # Encode and Display After Image
                secret_message = secret_message_entry.get()
                encoded_image_path = encode_image(file_path, secret_message)
                display_image(after_image, encoded_image_path)
            else:
                # Display Dropped Image
                display_image(dropped_image, file_path)
        elif file_extension in AUDIO_EXTENSIONS:
            # Play Audio
            play_audio(file_path)
        elif file_extension in VIDEO_EXTENSIONS:
            # TODO(GUI): Add a preview frame of the video like the images
            # ! and provide some indication that a file has been loaded.
            # Play Video
            play_video(root, file_path)
        else:
            messagebox.showinfo("Unsupported Format", "Unsupported file format for preview.")

def browse_file():
    file_path = filedialog.askopenfilename()
    process_file(file_path)


def encode_image(file_path, secret_message):
    # Encode the secret message into the image and save it as a new file
    encoded_image_path = file_path.replace(".", "_encoded.")
    stega.encode(file_path, secret_message, encoded_image_path)
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
        video_clip.preview(
            fps=24, audio=True,
            # threaded=True, winname="Video Preview" # ! Doesn't work
        )
    except Exception as e:
        messagebox.showerror("Error", f"Error playing video: {str(e)}")

def main():
    global before_image, after_image, dropped_image, secret_message_entry, root

    pygame.mixer.init()
    pygame.font.init()

    root = TkinterDnD.Tk()
    root.title("Steganography")
    root.geometry("800x600")  # Increased height to accommodate the new frame
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

    # Create a frame to hold the dropped content and drop logic
    dropped_frame = Frame(root)
    dropped_frame.pack(pady=20)

    dropped_image_label = Label(dropped_frame, text="Dropped Image")
    dropped_image_label.pack()
    dropped_image = Label(dropped_frame)
    dropped_image.pack()

    drop_label = Label(root, text="Drag and drop a file here")
    drop_label.pack(pady=100)

    # Bind the drop event to the drop function
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', drop)

    # Secret message input box
    secret_message_label = Label(root, text="Enter Secret Message:")
    secret_message_label.pack()
    secret_message_entry = Entry(root, width=50)
    secret_message_entry.pack()

    # Button for adding files to show on before image
    browse_button = Button(root, text="Browse Files", command=browse_file)
    browse_button.pack()

    # TODO(GUI): Add a dropdown to choose number of LSBs.

    # TODO(GUI): Add a button to encode the secret message? Or encode on the fly?

    # TODO(GUI): Add a button to decode the secret message.

    # TODO(GUI): Add a button to open a file dialog for saving the encoded file.

    root.mainloop()

if __name__ == "__main__":
    main()
