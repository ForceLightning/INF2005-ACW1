import os
import sys

import io
from typing import Union
import wave

import PIL
from PIL import Image
import cv2

from steganography.encoder import *
from steganography.decoder import *


class Steganography:
    def __init__(self, *args, **kwargs):
        self.encoder = None
        self.decoder = None
        pass

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
        cover_file: Union[str, bytes, io.BytesIO, Image.Image, wave.Wave_read, cv2.VideoCapture],
        secret_data: Union[str, bytes, int],
        output_file: Union[str, io.BytesIO, None] = None
    ) -> Union[str, bytes, Image.Image, wave.Wave_write, cv2.VideoCapture, None]:
        """Encodes `secret_data` into `cover_file`

        Args:
            cover_file (Union[str, bytes, io.BytesIO, Image.Image, cv2.VideoCapture]): Cover file, file-like object or filepath to encode `secret_data` into
            secret_data (Union[str, bytes, int]): Data to encode into `cover_file`
            output_file (Union[str, io.BytesIO, None], optional): Output file or filepath to write encoded data to. Defaults to None.

        Raises:
            NotImplementedError: Method not implemented.
            FileNotFoundError: `cover_file` or `output_file` is not a valid filepath

        Returns:
            Union[bytes, Image.Image, cv2.VideoCapture, None]: Encoded data if `output_file` is not None, else of type `cover_file`
        """
        raise NotImplementedError("Method not implemented.")
        # TODO(IO): Check if `cover_file` is a valid filepath
        # TODO(IO): Check if `output_file` is a valid filepath (if not None)
        # TODO(IO): Open file handlers for `cover_file` and `output_file` (if not None)
        
        # TODO(Encoder): Initialise encoder based on `cover_file` type (image, audio, or video)
        # ! use self.encoder = ImageEncoder() or self.encoder = AudioEncoder() or self.encoder = VideoEncoder()

        # TODO(Encoder): Encode `secret_data` into `cover_file`
        # ! use self.encoder.encode(cover_file, secret_data, output_file)
        
        # TODO(IO): Save encoded data to `output_file` (if not None)
        # TODO(IO): Close file handlers for `cover_file` and `output_file` (if not None)

    def decode(
        self,
        encoded_file: Union[str, bytes, io.BytesIO,
                            Image.Image, cv2.VideoCapture]
    ) -> str:
        """Decodes `encoded_file` and returns the decoded data

        Args:
            encoded_file (Union[str, bytes, io.BytesIO, Image.Image, cv2.VideoCapture]): Encoded file, file-like object or filepath to decode

        Raises:
            NotImplementedError: Method not implemented.
            TypeError: `encoded_file` is not of type str, bytes, io.BytesIO, Image.Image, or cv2.VideoCapture

        Returns:
            str: Decoded data
        """
        raise NotImplementedError("Method not implemented.")
        # TODO(IO): Check if `encoded_file` is a valid filepath if of type str
        # TODO(IO): Open file handler for `encoded_file` if of type str
        
        # TODO(Decoder): Initialise decoder based on `encoded_file` type (image, audio, or video)
        # ! use self.decoder = ImageDecoder() or self.decoder = AudioDecoder() or self.decoder = VideoDecoder()
        
        # TODO(Decoder): Decode `encoded_file`
        # ! use self.decoder.decode(encoded_file)
        
        # TODO(IO): Close file handler for `encoded_file` if of type str
