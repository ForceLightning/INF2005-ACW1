import os
import sys

from tkinter import *
from tkinter.ttk import *

from steganography.steganography import Steganography


def main():
    root = Tk()
    root.title("Steganography")
    root.geometry("500x500")
    root.resizable(False, False)
    stega = Steganography()
    # TODO: Add and initialise widgets here

    # TODO(Widgets): Setup text input box for secret message
    # TODO(Widgets): Setup button to open file dialog to select cover, encoded, and/or output files.
    # TODO(Widgets): Add drag-and-drop functionality to select cover, encoded, and/or output files.

    # TODO(Widgets): Setup button to encode secret message into cover file.
    # ! use stega.encode(cover_file, secret_data, output_file)

    # TODO(Widgets): Setup button to decode secret message from encoded file.
    # ! use stega.decode(encoded_file)

    # TODO(Stega/Encoder): Encode secret message in text box into cover file and save to output file

    # TODO(Stega/Decoder): Display decoded secret message in text box

    # TODO(Preview): Display/play cover image/audio/video in main window (or in a new window)
    # ! maybe use system default image/audio/video viewer/player
    # ! write to a temporary file, or use a library like PIL, OpenCV, or PyGame

    root.mainloop()
    return


if __name__ == "__main__":
    main()
