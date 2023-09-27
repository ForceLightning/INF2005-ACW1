import io
import os
import sys

import warnings
import abc
from typing import Union, NamedTuple
from collections import namedtuple
import wave
from math import prod

import PIL
from PIL import Image
import cv2
import numpy as np

import steganography.util as util


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
    ) -> np.ndarray:
        """Encodes secret data into a cover frame using the specified number of LSBs

        Args:
            cover_file_bytes (numpy.ndarray): Image/Audio/Video frames as a numpy array
            secret_data (str): Data to encode into the cover file
            num_lsb (int): Number of LSBs to use for encoding

        Raises:
            ValueError: Insufficient bytes, need bigger image or less data.
            ValueError: Secret data has to be ASCII encoded.
            IndexError: num_lsb must be between 1 and 8

        Returns:
            numpy.ndarray: Encoded cover file
        """
        n_bytes = prod(cover_file_bytes.shape)
        bit_depth = cover_file_bytes.dtype.itemsize * 8
        if len(secret_data) != len(secret_data.encode()):
            raise ValueError("Secret data must be ASCII.")
        binary_secret_data = util._data_to_binarray(secret_data, num_lsb)
        and_mask = np.bitwise_or(
            (2 ** bit_depth - 1) - (2 ** num_lsb - 1),
            binary_secret_data
        )
        data_len = len(binary_secret_data)
        if data_len * bit_depth > n_bytes * num_lsb:
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
        # ensure that the bit depth is the same
        or_op = or_op.astype(cover_file_bytes.dtype)
        return or_op

    @abc.abstractmethod
    def read_file(self, filename) -> (np.ndarray, NamedTuple):
        """Reads a file and returns the bytes

        Args:
            filename (str): Filepath to the file to read

        Raises:
            FileNotFoundError: File not found
            io.UnsupportedOperation: Wrong filetype

        Returns:
            np.ndarray: File bytes
        """
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def write_file(self, data: np.ndarray, filename: str, params: NamedTuple = None):
        """Writes the encoded data to a file

        Args:
            data (np.ndarray): Encoded data
            filename (str): Filepath to write the encoded data to
            params (NamedTuple, optional): Parameters for the file. Defaults to None.

        Raises:
            FileNotFoundError: File not found
        """
        if os.path.isfile(filename):
            warnings.warn("File already exists. Overwriting file.", UserWarning)
        else:
            dir_to_file = os.path.dirname(filename)
            if not os.path.exists(dir_to_file):
                os.makedirs(dir_to_file, exist_ok=True)
                return

class ImageEncoder(Encoder):
    """ Class for encoding data into an image file
    """

    def encode(
        self,
        cover_file_bytes: np.ndarray,
        secret_data: str,
        num_lsb: int = 1,
    ) -> np.ndarray:
        stop_condition = "====="
        secret_data += stop_condition
        return super().encode(cover_file_bytes, secret_data, num_lsb)

    def read_file(self, filename) -> (np.ndarray, NamedTuple):
        if os.path.isfile(filename):
            ext = os.path.splitext(filename)[1][1:]
            if ext in util.IMAGE_EXTENSIONS:
                image = cv2.imread(filename)
                return image, None
            else:
                raise io.UnsupportedOperation(f"File with extension {ext} is not an image.")
        else:
            raise FileNotFoundError("File not found.")

    def write_file(self, data: np.ndarray, filename: str, params: NamedTuple = None):
        super().write_file(data, filename)
        cv2.imwrite(filename, data)


class AudioEncoder(Encoder):
    """This class is for encoding data into an audio file"""

    def encode(
        self,
        cover_file_bytes: np.ndarray,
        secret_data: str,
        num_lsb: int = 1,
    ) -> np.ndarray:
        stop_condition = "====="
        secret_data += stop_condition
        encoded_data = super().encode(cover_file_bytes, secret_data, num_lsb)
        return encoded_data

    def read_file(self, filename) -> (np.ndarray, NamedTuple):
        if os.path.isfile(filename): 
            ext = os.path.splitext(filename)[1][1:]
            if ext in util.AUDIO_EXTENSIONS:
                audio = wave.open(filename, mode="rb")
                audio_data = audio.readframes(audio.getnframes())
                audio_bits = audio.getsampwidth() * 8
                params = audio.getparams()
                match audio_bits:
                    case 8:
                        audio_data = np.frombuffer(audio_data, dtype=np.uint8)
                    case 16:
                        audio_data = np.frombuffer(audio_data, dtype=np.int16)
                    case 32:
                        audio_data = np.frombuffer(audio_data, dtype=np.int32)
                    case _:
                        audio_data = np.frombuffer(audio_data, dtype=np.uint8)
                audio_data = audio_data.reshape(-1, audio.getnchannels())
                return audio_data, params
            else:
                raise io.UnsupportedOperation(f"File with extension {ext} is not an audio file.")
        else:
            raise FileNotFoundError("File not found.")

    def write_file(self, data: np.ndarray, filename: str, params: NamedTuple = None):
        super().write_file(data, filename)
        audio = wave.open(filename, mode="wb")
        audio.setparams(params)
        audio.writeframes(data.tobytes())


class VideoEncoder(Encoder):
    """This class is for encoding data into a video file"""

    def encode(
        self,
        cover_file_bytes: np.ndarray,
        secret_data: str,
        num_lsb: int = 1,
    ) -> np.ndarray:
        stop_condition = "====="
        secret_data += stop_condition
        encoded_data = super().encode(cover_file_bytes, secret_data, num_lsb)
        return encoded_data

    def read_file(self, filename) -> (np.ndarray, NamedTuple):
        if os.path.isfile(filename):
            ext = os.path.splitext(filename)[1][1:]
            if ext in util.VIDEO_EXTENSIONS:
                video = cv2.VideoCapture(filename)
                video_params = namedtuple(
                    "VideoParams",
                    ["fps", "width", "height"]
                )(
                    video.get(cv2.CAP_PROP_FPS),
                    video.get(cv2.CAP_PROP_FRAME_WIDTH),
                    video.get(cv2.CAP_PROP_FRAME_HEIGHT)
                )
                video_data = []
                while video.isOpened():
                    ret, frame = video.read()
                    if ret:
                        video_data.append(frame)
                    else:
                        break
                video_data = np.array(video_data)
                return video_data, video_params
            else:
                raise io.UnsupportedOperation(f"File with extension {ext} is not a video.")
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

    def write_file(self, data: np.ndarray, filename: str, params: NamedTuple = None):
        super().write_file(data, filename)
        fps = params.fps
        video = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*"mp4v"), fps, (data.shape[1], data.shape[2]), True)
        for frame in data:
            video.write(frame)
        video.release()
