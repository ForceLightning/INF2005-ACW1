import os
import sys

import abc
import io
from typing import Union, NamedTuple
import wave
from math import prod

import PIL
from PIL import Image
import cv2
import numpy as np

from steganography.util import _data_to_binarray


class Encoder(abc.ABC):
    """ Abstract class for encoding data into a cover file
    """

    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def encode(
        self,
        cover_file_bytes: np.ndarray,
        secret_data: str,
        num_lsb: int = 1,
    ):
        """Encodes secret data into a cover frame using the specified number of LSBs

        Args:
            cover_file_bytes (numpy.ndarray): Image/Audio/Video frames as a numpy array
            secret_data (str): Data to encode into the cover file
            num_lsb (int): Number of LSBs to use for encoding

        Raises:
            ValueError: Insufficient bytes, need bigger image or less data.
            IndexError: num_lsb must be between 1 and 8
        """
        n_bytes = prod(cover_file_bytes.shape)
        bit_depth = cover_file_bytes.dtype.itemsize * 8
        binary_secret_data = _data_to_binarray(secret_data, num_lsb)
        and_mask = np.bitwise_or(
            (2 ** bit_depth - 1) - (2 ** num_lsb - 1),
            binary_secret_data
        )
        data_len = len(binary_secret_data)
        if data_len > n_bytes:
            raise ValueError(
                "[!] Insufficient bytes, use a larger image,"
                + " greater LSBs, or less data."
            )
        padding = n_bytes - data_len
        # padded values should be 255 for AND mask and 0 for OR mask
        and_mask = np.pad(
            and_mask,
            (0, padding),
            constant_values=255
        )
        # reshape to the shape of the cover file
        and_mask = and_mask.reshape(*cover_file_bytes.shape)
        or_mask = np.pad(binary_secret_data, (0, padding), constant_values=0)
        or_mask = or_mask.reshape(*cover_file_bytes.shape)
        # encode data into image with the bitwise operations A + (A * B)
        and_op = np.bitwise_and(cover_file_bytes, and_mask)
        or_op = np.bitwise_or(and_op, or_mask)
        return or_op

    @abc.abstractmethod
    def read_file(self, filename) -> np.ndarray:
        """Reads a file and returns the bytes

        Args:
            filename (str): Filepath to the file to read

        Raises:
            FileNotFoundError: File not found

        Returns:
            np.ndarray: File bytes
        """
        raise NotImplementedError("Method not implemented.")


class ImageEncoder(Encoder):
    """ Class for encoding data into an image file
    """

    def encode(
        self,
        cover_file_bytes: np.ndarray,
        secret_data: str,
        num_lsb: int = 1,
    ):
        stop_condition = "====="
        secret_data += stop_condition
        return super().encode(cover_file_bytes, secret_data, num_lsb)

    def read_file(self, filename) -> np.ndarray:
        if os.path.isfile(filename) and os.path.splitext(filename)[1] in [".png", ".jpg", ".jpeg"]:
            image = cv2.imread(filename)
            return image

class AudioEncoder(Encoder):
    """This class is for encoding data into an audio file"""

    def encode(
        self,
        cover_file_bytes: np.ndarray,
        secret_data: str,
        num_lsb: int = 1,
    ):
        stop_condition = "====="
        secret_data += stop_condition
        encoded_data = super().encode(cover_file_bytes, secret_data, num_lsb)
        return encoded_data

    def read_file(self, filename) -> (np.ndarray, NamedTuple):
        if os.path.isfile(filename) and os.path.splitext(filename)[1] == ".wav":
            audio = wave.open(filename, mode="rb")
            audio_data = audio.readframes(audio.getnframes())
            audio_data = np.frombuffer(audio_data, dtype=np.uint8)
            return audio_data, audio.getparams()


class VideoEncoder(Encoder):
    """This class is for encoding data into a video file"""

    def encode(
        self,
        cover_file_bytes: np.ndarray,
        secret_data: str,
        num_lsb: int = 1,
    ):
        stop_condition = "====="
        secret_data += stop_condition
        encoded_data = super().encode(cover_file_bytes, secret_data, num_lsb)
        return encoded_data

    def read_file(self, filename) -> np.ndarray:
        if os.path.isfile(filename) and os.path.splitext(filename)[1] in [".mp4", ".avi"]:
            video = cv2.VideoCapture(filename)
            return video
        else:
            raise FileNotFoundError("File not found.")

    def batched_encode(
        self,
        video_capture: cv2.VideoCapture,
        secret_data: str,
        num_lsb: int = 1,
        minibatch_size: int = 30,
    ):
        raise NotImplementedError("Method not implemented.")
