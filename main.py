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
# steganography/util.py

# Define image file extensions

# image used <a href="https://www.flaticon.com/free-icons/equalizer" title="equalizer icons">Equalizer icons created by Ehtisham Abid - Flaticon</a>
# Initialize Steganography and Decoders
stega = Steganography()

# TODO(Zibin): Create the layout as discussed

# TODO(Chris): Add a preview frame of the video like the images

# TODO(Zexi): Audio placeholder image and playback functionality

# TODO(Sherlyn): Handle temp file deletion on exit

# TODO(Yok): Finish the project

# Function to handle drop event
def drop(event):
    global dropped_file_path
    dropped_file_path = event.data.strip("{}")
    print(f"File Path: {dropped_file_path}") # For debug
    process_file(dropped_file_path, is_dropped=True)

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
                secret_message = secret_message_entry.get("1.0", 'end-1c')
                # TODO(GUI): Use the selected number of LSBs
                encoded_image_path = encode_image(file_path, secret_message)
                global after_image_pil  # Declare it as global to update it
                after_image_pil = Image.open(encoded_image_path)  # Update after_image_pil
                display_image(after_image, encoded_image_path)
            else:
                # Display Dropped Image
                display_image(dropped_image, file_path)
        elif file_extension in AUDIO_EXTENSIONS:
            # Play Audio
            display_image(before_image, "tests/audioimage.png")
            play_file_button_encode = Button(encode_button_frame, text="Play File", command=lambda: play_audio(file_path))
            play_file_button_encode.grid(row=0, column=1)
            # play_audio(file_path)
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

# Function to encode image
def encode_image(file_path, secret_message, save_path=None, num_lsb=1):
    # If a save path is provided, use it; otherwise, create a new file name
    encoded_image_path = save_path if save_path else file_path.replace(".", "_encoded.")
    stega.encode(file_path, secret_message, encoded_image_path, num_lsb)
    return encoded_image_path

# Function to decode image
def decode_image():
    global dropped_file_path 
    if dropped_file_path:
        try:
            decoded_message = stega.decode(dropped_file_path)
            messagebox.showinfo("Decoded Message", f"The decoded message is: {decoded_message}")
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
    if after_image_pil:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            after_image_pil.save(save_path)
            messagebox.showinfo("Success", "After Image saved successfully.")
    elif dropped_file_path:
        file_extension = dropped_file_path.split('.')[-1].lower()
        if file_extension in IMAGE_EXTENSIONS:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                secret_message = secret_message_entry.get()
                # Encode the image and save it to the specified path
                encode_image(dropped_file_path, secret_message, save_path, num_lsb)
                messagebox.showinfo("Success", "Encoded image saved successfully.")
        elif file_extension in AUDIO_EXTENSIONS:
            save_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
            if save_path:
                secret_message = secret_message_entry.get()
                encode_av(dropped_file_path, secret_message, save_path)
                messagebox.showinfo("Success", "Encoded audio saved successfully.")
        elif file_extension in VIDEO_EXTENSIONS:
            save_path = filedialog.asksaveasfilename(defaultextension=".mov", filetypes=[("MOV files", "*.mov")])
            if save_path:
                secret_message = secret_message_entry.get()
                encode_av(dropped_file_path, secret_message, save_path)
                messagebox.showinfo("Success", "Encoded video saved successfully.")
    else:
        messagebox.showwarning("No File", "No dropped file to encode.")

# Clear all file
def clear_images():
    global dropped_file_path, after_image_pil
    # Clear the images
    before_image.config(image='')
    after_image.config(image='')
    dropped_image.config(image='')
    # Reset the global variables
    dropped_file_path = None
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

dropped_file_path = None
after_image_pil = None


def main():
    global before_image, after_image, dropped_image, secret_message_entry, lsb_combobox, root,encode_frame,encode_button_frame
    pygame.mixer.init()
    pygame.font.init()

    root = TkinterDnD.Tk()
    root.title("Steganography")
    root.geometry("900x450")
    root.resizable(False, False)

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
    load_file_button_encode.grid(row=0, column=0)
    
    # play_file_button_encode = Button(encode_button_frame, text="Play File", command=lambda: play_file(file_path))
    # play_file_button_encode.grid(row=0, column=1)

    before_image = Label(encode_frame)
    before_image.pack()

    
    # Decode Frame #
    decode_frame = Frame(root)
    decode_frame.grid(row=0, column=1, padx=10, pady=10)

    decode_label = Label(decode_frame, text="Decode", font=("Helvetica", 16))
    decode_label.pack()

    # Decode button frame
    decode_button_frame = Frame(decode_frame)
    decode_button_frame.pack()

    # Decode buttons
    load_file_button_decode = Button(decode_button_frame, text="Load File")
    load_file_button_decode.grid(row=0, column=0)

    play_file_button_decode = Button(decode_button_frame, text="Play File")
    play_file_button_decode.grid(row=0, column=1)

    save_file_button = Button(decode_button_frame, text="Save File", command=save_encoded_file)
    save_file_button.grid(row=0, column=2)

    after_image = Label(decode_frame)
    after_image.pack()

    
    # Secret Message Frame #
    secret_message_frame = Frame(root)
    secret_message_frame.grid(row=1, columnspan=2, padx=50)

    secret_message_entry = Text(secret_message_frame, width=80, height=10)
    secret_message_entry.pack(fill=X)

    # Frame for the decode encode buttons
    action_button_frame = Frame(root)
    action_button_frame.grid(row=2, columnspan=2)

    encode_button = Button(action_button_frame, text="Encode")
    encode_button.grid(row=0, column=0, padx=5, pady=5)

    decode_button = Button(action_button_frame, text="Decode", command=decode_image)
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

    # # Bind the drop event to the drop function
    # root.drop_target_register(DND_FILES)
    # root.dnd_bind('<<Drop>>', drop)

    # # Secret message input box
    # secret_message_label = Label(root, text="Enter Secret Message:")
    # secret_message_label.pack()
    # secret_message_entry = Entry(root, width=50)
    # secret_message_entry.pack()

    # # Dropdown to choose number of LSBs.
    # lsb_label = Label(root, text="Select Number of LSBs:")
    # lsb_label.pack()
    # lsb_combobox = Combobox(root, values=[1, 2, 3, 4, 5, 6, 7, 8])
    # lsb_combobox['state'] = 'readonly'
    # lsb_combobox.current(0) # Default to 1
    # lsb_combobox.pack()

    # # Button to decode the secret message.
    # decode_button = Button(root, text="Decode Message", command=decode_image)
    # decode_button.pack()

    # # Button to save the encoded file
    # save_button = Button(root, text="Save Encoded File", command=save_encoded_file)
    # save_button.pack()


    root.mainloop()

if __name__ == "__main__":
    main()
