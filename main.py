import os
import sys

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

#from steganography import Steganography
from steganography.decoder import ImageDecoder, AudioDecoder, VideoDecoder
from steganography.encoder import ImageEncoder, AudioEncoder, VideoEncoder


# Initialize Steganography and Decoders
#stega = Steganography()
image_decoder = ImageDecoder()
audio_decoder = AudioDecoder()
video_decoder = VideoDecoder()
image_encoder = ImageEncoder()
audio_encoder = AudioEncoder()
video_encoder = VideoEncoder()

def main():
    root = Tk()
    root.title("Steganography")
    root.geometry("500x500")
    root.resizable(False, False)
    #stega = Steganography()

    # TODO: Add and initialise widgets here

    # TODO(Widgets): Setup text input box for secret message
    secret_message_label = Label(root, text="Enter Secret Message:")
    secret_message_label.pack()
    secret_message_entry = Entry(root, width=50)
    secret_message_entry.pack()

    # TODO(Widgets): Setup button to open file dialog to select cover, encoded, and/or output files.
    def browse_file():
        file_path = filedialog.askopenfilename()
    browse_button = Button(root, text="Browse Files", command=browse_file)
    browse_button.pack()

    # TODO(Widgets): Add drag-and-drop functionality to select cover, encoded, and/or output files.
    

    # TODO(Widgets): Setup button to encode secret message into cover file.
    # ! use stega.encode(cover_file, secret_data, output_file)
   

    # TODO(Widgets): Setup button to decode secret message from encoded file.
    # ! use stega.decode(encoded_file)
    

    
    # TODO(Stega/Encoder): Encode secret message in text box into cover file and save to output file
    
    # TODO(Stega/Decoder): Display decoded secret message in text box

    # TODO(Preview): Display/play cover image/audio/video in main window (or in a new window)
    # ! maybe use system default image/audio/video viewer/player, write to a temporary file, or use a library like PIL, OpenCV, or PyGame
    
    root.mainloop()
    pass


if __name__ == "__main__":
    main()

# import os
# import sys
# import tkinter as tk
# from tkinter import filedialog
# from tkinter import messagebox
# from tkinter.ttk import *

# from steganography import Steganography
# from steganography.decoder import ImageDecoder, AudioDecoder, VideoDecoder
# from steganography.encoder import ImageEncoder, AudioEncoder, VideoEncoder

# # Initialize Steganography and Decoders
# stega = Steganography()
# image_decoder = ImageDecoder()
# audio_decoder = AudioDecoder()
# video_decoder = VideoDecoder()
# image_encoder = ImageEncoder()
# audio_encoder = AudioEncoder()
# video_encoder = VideoEncoder()

# # Function to handle the Encode button click
# def encode_message():
#     cover_file_path = cover_file_entry.get()
#     secret_message = secret_message_text.get("1.0", "end-1c")
#     output_file_path = output_file_entry.get()
    
#     try:
#         stega.encode(cover_file_path, secret_message, output_file_path)
#         messagebox.showinfo("Success", "Message encoded successfully!")
#     except Exception as e:
#         messagebox.showerror("Error", str(e))

# # Function to handle the Decode button click
# def decode_message():
#     encoded_file_path = encoded_file_entry.get()
    
#     try:
#         decoded_message = stega.decode(encoded_file_path)
#         decoded_message_text.delete("1.0", "end")
#         decoded_message_text.insert("1.0", decoded_message)
#         messagebox.showinfo("Success", "Message decoded successfully!")
#     except Exception as e:
#         messagebox.showerror("Error", str(e))

# # Function to open a file dialog and set the selected file path in an entry field
# def browse_file(entry_widget):
#     file_path = filedialog.askopenfilename()
#     entry_widget.delete(0, "end")
#     entry_widget.insert(0, file_path)

# # Create the main window
# root = tk.Tk()
# root.title("Steganography")
# root.geometry("500x500")
# root.resizable(False, False)

# # Label for secret message input
# secret_message_label = tk.Label(root, text="Enter Secret Message:")
# secret_message_label.pack()

# # Text input box for secret message
# secret_message_text = tk.Text(root, height=5, width=40)
# secret_message_text.pack()

# # Label for cover file input
# cover_file_label = tk.Label(root, text="Select Cover File:")
# cover_file_label.pack()

# # Entry field for cover file path
# cover_file_entry = tk.Entry(root, width=40)
# cover_file_entry.pack()

# # Button to browse for cover file
# cover_file_browse_button = tk.Button(root, text="Browse", command=lambda: browse_file(cover_file_entry))
# cover_file_browse_button.pack()

# # Label for output file input
# output_file_label = tk.Label(root, text="Select Output File:")
# output_file_label.pack()

# # Entry field for output file path
# output_file_entry = tk.Entry(root, width=40)
# output_file_entry.pack()

# # Button to browse for output file
# output_file_browse_button = tk.Button(root, text="Browse", command=lambda: browse_file(output_file_entry))
# output_file_browse_button.pack()

# # Button to encode secret message
# encode_button = tk.Button(root, text="Encode", command=encode_message)
# encode_button.pack()

# # Label for encoded file input
# encoded_file_label = tk.Label(root, text="Select Encoded File:")
# encoded_file_label.pack()

# # Entry field for encoded file path
# encoded_file_entry = tk.Entry(root, width=40)
# encoded_file_entry.pack()

# # Button to browse for encoded file
# encoded_file_browse_button = tk.Button(root, text="Browse", command=lambda: browse_file(encoded_file_entry))
# encoded_file_browse_button.pack()

# # Button to decode secret message
# decode_button = tk.Button(root, text="Decode", command=decode_message)
# decode_button.pack()

# # Text widget to display decoded message
# decoded_message_text = tk.Text(root, height=5, width=40)
# decoded_message_text.pack()

# root.mainloop()
