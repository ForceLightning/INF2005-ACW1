import os
import sys

import io
from typing import Union
import wave

import numpy as np
import cv2

from steganography.encoder import *
from steganography.decoder import *
from steganography.util import IMAGE_EXTENSIONS, AUDIO_EXTENSIONS, VIDEO_EXTENSIONS

class Steganography:
    """Class for encoding and decoding data into a cover file using LSB steganography
    """
    def __init__(self):
        self.encoder = None
        self.decoder = None
        self.encoded_data = None
        self.encoded_data_params = None

    def _to_bin(
        self,
        data: Union[str, bytes, int]
    ) -> str:
        """Converts `data` to binary format as string

        Args:
            data (Union[str, bytes, int]): Data of type str, bytes, or int

        Returns:
            str: Binary representation of `data`
        """
        raise NotImplementedError("Method not implemented.")

    def encode(
        self,
        cover_file: str,
        secret_data: str,
        output_file: Union[str, None] = None
    ) -> Union[str, bytes, np.ndarray, wave.Wave_write, cv2.VideoCapture, None]:
        """Encodes `secret_data` into `cover_file`

        Args:
            cover_file (Union[str, bytes, io.BytesIO, Image.Image, cv2.VideoCapture]):
                Cover file, file-like object or filepath to encode `secret_data` into
            secret_data (Union[str, bytes, int]): Data to encode into `cover_file`
            output_file (Union[str, io.BytesIO, None], optional):
                Output file or filepath to write encoded data to. Defaults to None.

        Raises:
            NotImplementedError: Method not implemented.
            FileNotFoundError: `cover_file` or `output_file` is not a valid filepath

        Returns:
            Union[bytes, Image.Image, cv2.VideoCapture, None]:
                Encoded data if `output_file` is not None, else of type `cover_file`
        """
        # Check if `cover_file` is a valid filepath
        if not os.path.isfile(cover_file):
            raise FileNotFoundError(f"File '{cover_file}' not found.")
        else:
            # Initialise encoder based on `cover_file` type (image, audio, or video)
            ext = os.path.splitext(cover_file)[1][1:]
            if ext in IMAGE_EXTENSIONS:
                self.encoder = ImageEncoder()
                self.decoder = ImageDecoder()
            elif ext in AUDIO_EXTENSIONS:
                self.encoder = AudioEncoder()
                self.decoder = AudioDecoder()
            elif ext in VIDEO_EXTENSIONS:
                self.encoder = VideoEncoder()
                self.decoder = VideoDecoder()
            else:
                raise io.UnsupportedOperation(f"File extension '{ext}' not supported.")
            data, _ = self.encoder.read_file(cover_file)
            # Encode `secret_data` into `cover_file`
            self.encoded_data = self.encoder.encode(data, secret_data)
        # Check if `output_file` is a valid filepath (if not None)
        match output_file:
            case str():
                if not os.path.isfile(output_file):
                    # create file
                    path_to_file = os.path.dirname(output_file)
                    if path_to_file:
                        os.makedirs(path_to_file, exist_ok=True)

            # Open file handlers for `cover_file` and `output_file` (if not None)
            # Save encoded data to `output_file` (if not None)
                self.encoder.write_file(self.encoded_data, output_file)
            case _:
                return self.encoded_data

    def decode(
        self,
        encoded_file: Union[str, bytes, io.BytesIO,
                            Image.Image, cv2.VideoCapture]
    ) -> str:
        """Decodes `encoded_file` and returns the decoded data

        Args:
            encoded_file (Union[str, bytes, io.BytesIO, Image.Image, cv2.VideoCapture]):
                Encoded file, file-like object or filepath to decode

        Raises:
            NotImplementedError: Method not implemented.
            TypeError: `encoded_file` is not of type str, bytes,
            io.BytesIO, Image.Image, or cv2.VideoCapture

        Returns:
            str: Decoded data
        """
        #raise NotImplementedError("Method not implemented.")
        # To hold file data
        data = None 
        # Check if `encoded_file` is a valid filepath
        if not os.path.isfile(encoded_file):
            raise FileNotFoundError(f"File '{encoded_file}' not found.")
        else:
            # Check if `encoded_file` is a valid filepath if of type str (if not None)
            match decoded_data:
                case str():
                    # Initialise decoder based on `encoded_file` type (image, audio, or video)
                    ext = os.path.splitext(encoded_file)[1]
                    if ext in IMAGE_EXTENSIONS:
                        self.encoder = ImageEncoder()
                        self.decoder = ImageDecoder()
                    elif ext in AUDIO_EXTENSIONS:
                        self.encoder = AudioEncoder()
                        self.decoder = AudioDecoder()
                    elif ext in VIDEO_EXTENSIONS:
                        self.encoder = VideoEncoder()
                        self.decoder = VideoDecoder()
                    else:
                        raise io.UnsupportedOperation(f"File extension '{ext}' not supported.")

                    # Read file to be decoded
                    data, _ = self.decoder.read_file(encoded_file)
                    # Decode `encoded_file`
                    decoded_data = self.decoder.decode(data)


                case _:
                # return nothing if `encoded_data` is not a string
                    return None

        return decoded_data
        # TODO(IO): Open file handler for `decoded_data` if of type str
        # Check if `encoded_file` is a valid filepath (if not None)
        # TODO(IO): Close file handler for `encoded_file` if of type str