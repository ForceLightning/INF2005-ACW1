import os
import sys
import threading

from typing import Union
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
from numpy import place
import pygame
from moviepy.editor import VideoFileClip
from tkinterdnd2 import TkinterDnD, DND_FILES
from steganography.encoder import AudioEncoder, ImageEncoder, VideoEncoder

from steganography.steganography import Steganography
from steganography.util import IMAGE_EXTENSIONS, AUDIO_EXTENSIONS, VIDEO_EXTENSIONS
# steganography/util.py

# Define image file extensions

# image used <a href="https://www.flaticon.com/free-icons/equalizer" title="equalizer icons">Equalizer icons created by Ehtisham Abid - Flaticon</a>
# Initialize Steganography and Decoders
stega = Steganography()
temp_path = None

# TODO(Zibin): Create the layout as discussed

# TODO(Chris): Add a preview frame of the video like the images

# TODO(Zexi): Audio placeholder image and playback functionality

# TODO(Sherlyn): Handle temp file deletion on exit

# TODO(Yok): Finish the project

# Function to handle drop event


def drop(event):
    global dropped_file_path, before_image, after_image
    dropped_file_path = event.data.strip("{}")
    print(f"File Path: {dropped_file_path}")  # For debug

    drop_target = event.widget.winfo_name()  # Get the name of the widget where the file was dropped
    process_file(dropped_file_path, drop_target)
    #print("Widget Object:", event.widget)
    #print("Widget Name:", event.widget.winfo_name())
    #print("Widget Class:", event.widget.winfo_class())




def display_image(label, image: Union[str, Image.Image]):
    if isinstance(image, str):
        image = Image.open(image)
    # Limit the size of the displayed image
    image.thumbnail((200, 200))
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.photo = photo


def process_file(file_path, placeholder_image_location, encode=True):
    if file_path:
        file_extension = os.path.splitext(file_path)[1][1:].lower()
        print(f"File Extension: {file_extension}")
        if file_extension in IMAGE_EXTENSIONS:
            display_image(placeholder_image_location, file_path)
        elif file_extension in AUDIO_EXTENSIONS:
            # Play Audio
            display_image(placeholder_image_location, "tests/audioimage.png")
            if encode:
                play_file_button_encode = Button(
                    encode_button_frame, text="Play File", command=lambda: play_audio(file_path))
                play_file_button_encode.grid(row=0, column=1)
            else:
                play_file_button_decode = Button(
                    decode_button_frame, text="Play File", command=lambda: play_audio(file_path))
                play_file_button_decode.grid(row=0, column=1)
            # play_audio(file_path)
        elif file_extension in VIDEO_EXTENSIONS:
            video = cv2.VideoCapture(file_path)
            ret, frame = video.read()
            if ret:
                # Display Before Image
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(frame)
                display_image(placeholder_image_location, pil_image)
                if encode:
                    play_file_button_encode = Button(
                        encode_button_frame, text="Play File", command=lambda: play_video(root, file_path))
                    play_file_button_encode.grid(row=0, column=1)
                else:
                    play_file_button_decode = Button(
                        decode_button_frame, text="Play File", command=lambda: play_video(root, file_path))
                    play_file_button_decode.grid(row=0, column=1)
        else:
            messagebox.showinfo("Unsupported Format",
                                "Unsupported file format for preview.")


def browse_file():
    global dropped_file_path, before_image, play_file_button_encode, encode_button_frame
    dropped_file_path = filedialog.askopenfilename()
    process_file(dropped_file_path, before_image)


def browse_file_decode():
    global after_image_path, after_image, play_file_button_decode, decode_button_frame
    after_image_path = filedialog.askopenfilename()
    if after_image_path:
        process_file(after_image_path, after_image, False)

# Function to encode image
def encode_image(file_path, secret_message, save_path=None, num_lsb=1):
    global after_image_path
    # If a save path is provided, use it; otherwise, create a new file name
    after_image_path = stega.encode(file_path, secret_message, True, num_lsb)
    return after_image_path

# Function to decode image


def decode_image():
    global after_image_path
    if after_image_path:
        try:
            num_lsb = int(lsb_combobox.get())
            decoded_message = stega.decode(after_image_path, num_lsb)
            # messagebox.showinfo("Decoded Message",
            #                     f"The decoded message is: {decoded_message}")
            secret_message_entry.delete("1.0", END)
            secret_message_entry.insert("1.0", decoded_message)
        except Exception as e:
            messagebox.showerror("Error", f"Error decoding message: {str(e)}")
    else:
        messagebox.showwarning("No File", "No dropped file to decode.")

# Function to encode audio and video
def encode_av(file_path, secret_message, output_path):
    try:
        stega.encode(file_path, secret_message, output_path)
    except Exception as e:
        messagebox.showerror("Error", f"Error encoding audio/video: {str(e)}")

# Function to save the encoded file
def save_encoded_file():
    global dropped_file_path, after_image_pil
    num_lsb = int(lsb_combobox.get())
    secret_message = secret_message_entry.get("1.0", 'end-1c')
    if after_image_pil:
        save_path = filedialog.asksaveasfilename(
            defaultextension=".bmp", filetypes=[("BMP files", "*.BMP")])
        if save_path:
            after_image_pil.save(save_path)
            messagebox.showinfo("Success", "After Image saved successfully.")
    elif dropped_file_path:
        file_extension = dropped_file_path.split('.')[-1].lower()
        if file_extension in IMAGE_EXTENSIONS:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".bmp", filetypes=[("BMP files", "*.bmp")])
        elif file_extension in AUDIO_EXTENSIONS:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        elif file_extension in VIDEO_EXTENSIONS:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".mov", filetypes=[("MOV files", "*.mov")])
        else:
            messagebox.showerror("Error", "Unsupported file format.")
            return
        if save_path:
            try:
                stega.encode(dropped_file_path, secret_message,
                             save_path, num_lsb)
            except Exception as e:
                messagebox.showerror("Error", f"Error encoding file: {str(e)}")
    else:
        messagebox.showwarning("No File", "No dropped file to encode.")


def encode_file():
    global dropped_file_path, after_image_pil, temp_path, play_file_button_decode, decode_button_frame, after_image_path
    if dropped_file_path:
        secret_message = secret_message_entry.get("1.0", 'end-1c')
        if not secret_message:
            messagebox.showwarning(
                "No Message", "No secret message to encode.")
            return
        if not dropped_file_path:
            messagebox.showwarning("No File", "No dropped file to encode.")
            return
        num_lsb = int(lsb_combobox.get())
        try:
            temp_path = stega.encode(
                dropped_file_path, secret_message, True, num_lsb)
            after_image_path = temp_path
            match stega.encoder:
                case ImageEncoder():
                    display_image(after_image, temp_path)
                case AudioEncoder():
                    display_image(after_image, "tests/audioimage.png")
                    play_file_button_decode = Button(
                        decode_button_frame, text="Play File", command=lambda: play_audio(temp_path))
                case VideoEncoder():
                    video = cv2.VideoCapture(temp_path)
                    ret, frame = video.read()
                    if ret:
                        # Display after Image
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        after_image_pil = Image.fromarray(frame)
                        display_image(after_image, after_image_pil)
                    play_file_button_decode = Button(
                        decode_button_frame, text="Play File", command=lambda: play_video(root, temp_path))
        except Exception as e:
            messagebox.showerror("Error", f"Error encoding file: {str(e)}")

# Clear all file
def clear_images():
    global dropped_file_path, after_image_pil, after_image_path
    # Clear the images
    before_image.config(image='')
    after_image.config(image='')
    dropped_image.config(image='')
    # Reset the global variables
    dropped_file_path = None
    after_image_path = None
    after_image_pil = None


def play_audio(file_path):
    def audio_thread():
        try:
            print("Starting audio playback")
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            pygame.event.wait()  # Wait for the audio to finish playing
        except pygame.error as e:
            print(f"Error playing audio: {str(e)}")

    audio_playback_thread = threading.Thread(target=audio_thread)
    audio_playback_thread.start()


def play_video(root, file_path):
    video_thread = threading.Thread(
        target=play_video_clip, args=(root, file_path))
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


dropped_file_path = None
after_image_pil = None
after_image_path = None


def main():
    global before_image, after_image, dropped_image, secret_message_entry, lsb_combobox, root, encode_frame, encode_button_frame, decode_frame, decode_button_frame, after_image_path
    pygame.mixer.init()
    pygame.font.init()

    root = TkinterDnD.Tk()
    root.title("Steganography")
    root.geometry("835x700")
    root.resizable(False, False)

    # Bind the drop event to the drop function
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', drop)

    # Encode Frame #
    encode_frame = Frame(root)
    encode_frame.grid(row=0, column=0, padx=10, pady=10)

    encode_label = Label(encode_frame, text="Encode", font=("Helvetica", 16))
    encode_label.pack()

    # Encode button frame
    encode_button_frame = Frame(encode_frame)
    encode_button_frame.pack()

    # Encode buttons

    load_file_button_encode = Button(encode_button_frame, text="Load File", command=browse_file)
    load_file_button_encode.grid(row=0, column=0, padx=40)

    lsb_frame = Frame(encode_button_frame)
    lsb_frame.grid(row=1, column=0)

    lsb_label = Label(lsb_frame, text="Select Number of LSBs:")
    lsb_label.grid(row=1, column=0)  # Place it under the encode buttons
    lsb_combobox = Combobox(lsb_frame, values=[1, 2, 3, 4, 5, 6])
    lsb_combobox['state'] = 'readonly'
    lsb_combobox.current(0)  # Default to 1
    lsb_combobox.grid(row=1, column=1) 


    # play_file_button_encode = Button(encode_button_frame, text="Play File", command=lambda: play_file(file_path))
    # play_file_button_encode.grid(row=0, column=1)
    before_image = Label(encode_frame, name='before_image', width=60) 
    before_image.pack()
    before_image.drop_target_register(DND_FILES)
    before_image.dnd_bind('<<Drop>>', drop)

    # Decode Frame #
    decode_frame = Frame(root)
    decode_frame.grid(row=0, column=1, padx=10, pady=10)

    decode_label = Label(decode_frame, text="Decode", font=("Helvetica", 16))
    decode_label.pack()

    # Decode button frame
    decode_button_frame = Frame(decode_frame)
    decode_button_frame.pack()

    # Decode buttons
    load_file_button_decode = Button(decode_button_frame, text="Load File", command=browse_file_decode)
    load_file_button_decode.grid(row=0, column=0)

    play_file_button_decode = Button(decode_button_frame, text="Play File")
    play_file_button_decode.grid(row=0, column=1)

    save_file_button = Button(
        decode_button_frame, text="Save File", command=save_encoded_file)
    save_file_button.grid(row=0, column=2)

    after_image = Label(decode_frame, name='after_image', width=60)  # Add a name for identification
    after_image.pack()
    after_image.drop_target_register(DND_FILES)
    after_image.dnd_bind('<<Drop>>', drop)

    # Secret Message Frame #
    secret_message_frame = Frame(root)
    secret_message_frame.grid(row=1, columnspan=2, padx=50)
    secret_message_label = Label(root, text="Enter Secret Message:")
    secret_message_entry = Text(secret_message_frame, width=80, height=10)
    secret_message_entry.pack(fill=X)

    # Frame for the decode encode buttons
    action_button_frame = Frame(root)
    action_button_frame.grid(row=2, columnspan=2)

    encode_button = Button(action_button_frame,
                           text="Encode", command=encode_file)
    encode_button.grid(row=0, column=0, padx=5, pady=5)

    decode_button = Button(action_button_frame,
                           text="Decode", command=decode_image)
    decode_button.grid(row=0, column=1, pady=5)

    # global before_image, after_image, dropped_image, secret_message_entry, root, lsb_combobox
    # pygame.mixer.init()
    # pygame.font.init()

    # root = TkinterDnD.Tk()
    # root.title("Steganography")
    # root.geometry("1200x900")  # Increased height to accommodate the new frame
    # root.resizable(False, False)

    # # Create a frame to hold the before and after images
    # frame = Frame(root)
    # frame.pack()

    # # Create Labels for before and after images
    # before_image_label = Label(frame, text="Before Image")
    # before_image_label.grid(row=0, column=0, padx=10, pady=10)
    # before_image = Label(frame)
    # before_image.grid(row=1, column=0, padx=10, pady=10)

    # after_image_label = Label(frame, text="After Image")
    # after_image_label.grid(row=0, column=1, padx=10, pady=10)
    # after_image = Label(frame)
    # after_image.grid(row=1, column=1, padx=10, pady=10)

    # button_frame = Frame(root)
    # button_frame.pack(pady=20)

    # # Button for adding files to show on before image
    # browse_button = Button(button_frame, text="Select File To Encode", command=browse_file)
    # browse_button.grid(row=0, column=0, padx=10)

    # # Button to clear the images
    # clear_button = Button(button_frame, text="Clear Images", command=clear_images)
    # clear_button.grid(row=0, column=1, padx=10)

    # # Create a frame to hold the dropped content and drop logic
    # dropped_frame = Frame(root)
    # dropped_frame.pack(pady=20)

    # dropped_image_label = Label(dropped_frame, text="Dropped Image")
    # dropped_image_label.pack()
    # dropped_image = Label(dropped_frame)
    # dropped_image.pack()

    # drop_label = Label(root, text="Drag and drop a file here")
    # drop_label.pack(pady=100)

    

    # # Secret message input box
    # secret_message_label = Label(root, text="Enter Secret Message:")
    # secret_message_label.pack()
    # secret_message_entry = Entry(root, width=50)
    # secret_message_entry.pack()


    # # Button to decode the secret message.
    # decode_button = Button(root, text="Decode Message", command=decode_image)
    # decode_button.pack()

    # # Button to save the encoded file
    # save_button = Button(root, text="Save Encoded File", command=save_encoded_file)
    # save_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
