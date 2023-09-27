import os
import sys
import threading

from typing import Optional, Union
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, messagebox, Event
from functools import partial

from PIL import Image, ImageTk
import cv2
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


# TODO(Yok): Finish the project


def drop(event: Event, encode=True):
    """Handles the file drop event

    Args:
        event (tkinter.Event): Drop event
        encode (bool, optional): Selects which frame for the preview to be displayed in. Defaults to True. 
    """
    global dropped_file_path, before_image, after_image
    dropped_file_path = event.data.strip("{}")
    print(f"File Path: {dropped_file_path}")  # For debug

    if encode:
        process_file(dropped_file_path, before_image, encode)
    else:
        process_file(dropped_file_path, after_image, encode)


def display_image(label: Label, image: Union[str, Image.Image]):
    """Displays the image in the specified label

    Args:
        label (Label): Label to display the image in
        image (Union[str, Image.Image]): Image object or file path of the image to be displayed
    """
    if isinstance(image, str):
        image = Image.open(image)
    # Limit the size of the displayed image
    image.thumbnail((200, 200))
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.photo = photo


def process_file(
    file_path: str,
    placeholder_image_location: Label,
    encode: bool = True
):
    """Processes the dropped file and displays it in the appropriate frame

    Args:
        file_path (str): File path of the dropped file
        placeholder_image_location (str): Location of the placeholder image to be updated
        encode (bool, optional): Selects which frame for the preview to be displayed in. Defaults to True.
    """
    global after_image_path
    if placeholder_image_location == 'before_image':
        display_image(before_image, file_path)
    elif placeholder_image_location == 'after_image':
        display_image(after_image, file_path)
        after_image_path = file_path
    elif file_path:
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
    """Opens a file dialog to browse for a file to encode
    """
    global dropped_file_path, before_image, play_file_button_encode, encode_button_frame
    dropped_file_path = filedialog.askopenfilename()
    process_file(dropped_file_path, before_image)


def browse_file_decode():
    """Decodes the file and displays the decoded message in the secret message entry box
    """
    global after_image_path, after_image, play_file_button_decode, decode_button_frame
    after_image_path = filedialog.askopenfilename()
    if after_image_path:
        process_file(after_image_path, after_image, False)


def encode_image(
    file_path: str,
    secret_message: str,
    save_path: Union[str, bool] = True,
    num_lsb: Optional[int] = 1
) -> str:
    """Encodes the secret message into the image

    Args:
        file_path (str): Input cover filepath
        secret_message (str): Secret message to encode
        save_path (str, optional): Output save path. Defaults to None.
        num_lsb (int, optional): Number of LSBs to use. Defaults to 1.

    Returns:
        str: Output save path
    """
    global after_image_path
    # If a save path is provided, use it; otherwise, create a new file name
    after_image_path = stega.encode(
        file_path, secret_message, save_path, num_lsb)
    secret_message_entry.delete("1.0", END)
    return after_image_path


def decode_image():
    """Decodes the loaded image and displays the decoded message in the secret message entry box
    """
    global after_image_path
    if after_image_path:
        try:
            num_lsb = int(lsb_combobox.get())
            decoded_message = stega.decode(after_image_path, num_lsb)
            secret_message_entry.delete("1.0", END)
            secret_message_entry.insert("1.0", decoded_message)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error {type(e)} decoding message: {str(e)}")
    else:
        messagebox.showwarning("No File", "No dropped file to decode.")


def encode_av(
    file_path: str,
    secret_message: str,
    output_path: str
):
    """Encodes audio and video files

    Args:
        file_path (str): Input cover filepath
        secret_message (str): Secret message to encode
        output_path (str): Output filepath
    """
    try:
        stega.encode(file_path, secret_message, output_path)
    except Exception as e:
        messagebox.showerror(
            "Error", f"Error {type(e)} encoding audio/video: {str(e)}")


def save_encoded_file():
    """Saves the encoded file to a new file path
    """
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
                messagebox.showerror(
                    "Error", f"Error {type(e)} encoding file: {str(e)}")
    else:
        messagebox.showwarning("No File", "No dropped file to encode.")


def encode_file():
    """General encode function that handles encoding for all file types
    """
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
                    play_file_button_decode.grid(row=0, column=1)
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
                    play_file_button_decode.grid(row=0, column=1)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error {type(e)} encoding file: {str(e)}")


def clear_images():
    """Clears all the images and resets the global variables
    """
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
    """Plays the audio file

    Args:
        file_path (str): File path of the audio file
    """
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
    """Plays the video file

    Args:
        root (tkinter.Tk): Root window
        file_path (str): File path of the video file
    """
    video_thread = threading.Thread(
        target=_play_video, args=(root, file_path))
    video_thread.start()


def _play_video(root, file_path):
    """Internal function to play the video file

    Args:
        root (tkinter.Tk): Root window
        file_path (str): File path of the video file
    """
    try:
        video_clip = VideoFileClip(file_path)
        video_clip.preview(
            fps=24, audio=True,
            # threaded=True, winname="Video Preview" # ! Doesn't work
        )
    except Exception as e:
        messagebox.showerror("Error", f"Error playing video: {str(e)}")

def tempfile_cleanup():
    """Cleans up the temp files on exit
    """
    global temp_path
    # TODO(Sherlyn): Handle temp file deletion on exit
    pass

dropped_file_path = None
after_image_pil = None
after_image_path = None


def main():
    global before_image, after_image, dropped_image, secret_message_entry, lsb_combobox, root, encode_frame, encode_button_frame, decode_frame, decode_button_frame, after_image_path, play_file_button_decode
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
    # Encode buttons
    load_file_button_encode = Button(
        encode_button_frame, text="Load File", command=browse_file)
    load_file_button_encode.grid(row=0, column=0, padx=5)

    encode_button_frame.pack()

    # Drag and drop location
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
    load_file_button_decode = Button(
        decode_button_frame, text="Load File", command=browse_file_decode)
    load_file_button_decode.grid(row=0, column=0)

    play_file_button_decode = Button(decode_button_frame, text="Play File")
    play_file_button_decode.grid(row=0, column=1)

    save_file_button = Button(
        decode_button_frame, text="Save File", command=save_encoded_file)
    save_file_button.grid(row=0, column=2)

    # Drag and drop location
    after_image = Label(decode_frame, name='after_image',
                        width=60)  # Add a name for identification
    after_image.pack()
    after_image.drop_target_register(DND_FILES)
    after_image.dnd_bind('<<Drop>>', partial(drop, encode=False))

    # Secret Message Frame #
    secret_message_frame = Frame(root)
    secret_message_frame.grid(row=1, columnspan=2, padx=50)
    secret_message_label = Label(root, text="Enter Secret Message:")
    secret_message_entry = Text(secret_message_frame, width=80, height=10)
    secret_message_entry.pack(fill=X)

    # Frame for the decode encode buttons
    action_button_frame = Frame(root)
    action_button_frame.grid(row=2, columnspan=3)

    lsb_frame = Frame(action_button_frame)
    lsb_frame.grid(row=0, column=0)

    lsb_label = Label(lsb_frame, text="Select Number of LSBs:")
    # Place it under the encode buttons
    lsb_label.grid(row=0, column=0, padx=5, pady=5)
    lsb_combobox = Combobox(lsb_frame, values=[1, 2, 3, 4, 5, 6])
    lsb_combobox['state'] = 'readonly'
    lsb_combobox.current(0)  # Default to 1
    lsb_combobox.grid(row=0, column=1)

    encode_button = Button(action_button_frame,
                           text="Encode", command=encode_file)
    encode_button.grid(row=0, column=1, padx=5, pady=5)

    decode_button = Button(action_button_frame,
                           text="Decode", command=decode_image)
    decode_button.grid(row=0, column=2, pady=5)

    root.protocol("WM_DELETE_WINDOW", tempfile_cleanup)

    root.mainloop()


if __name__ == "__main__":
    main()
