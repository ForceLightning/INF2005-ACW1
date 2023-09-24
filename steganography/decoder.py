from collections import namedtuple
import os
import sys

import abc
import io
from typing import NamedTuple, Union
import wave
from math import prod
import re

import numpy as np
import cv2

import steganography.util as util
class Decoder(abc.ABC):
    def __init__(self, *args, **kwargs):
        self.decoded_data = ""

    @abc.abstractmethod
    def decode(
        self,
        encoded_data: np.ndarray[Union[int, np.uint8, np.int16, np.int32]],
        num_lsb: int = 1
    ) -> str:
        raise NotImplementedError("Method not implemented.")

    def _decode_frame(
        self,
        encoded_frame: np.ndarray[Union[int, np.uint8, np.int16, np.int32]],
        num_lsb: int = 1,
        early_stop: str = "=====",
        keep_early_stop: bool = False
    ) -> str:
        """Decodes the secret data from an encoded frame or frames

        Args:
            encoded_frame (np.ndarray[Union[int, np.uint8, np.int16, np.int32]]): encoded frame or frames
            num_lsb (int, optional): number of LSBs to decode from. Defaults to 1.
            early_stop (str, optional): stop condition. Defaults to "=====".
            keep_early_stop (bool, optional): keep the stop condition in the returned string. Defaults to False.

        Raises:
            ValueError: num_lsb must be between 1 and bit_depth

        Returns:
            str: decoded secret data
        """
        binary_data = ""
        self.decoded_data = ""
        bit_depth = encoded_frame.dtype.itemsize * 8
        if num_lsb > bit_depth or num_lsb < 1:
            raise ValueError(f"num_lsb must be between 1 and {bit_depth}")
        bitmask = 2 ** num_lsb - 1
        n_channels = encoded_frame.shape[-1]
        channel_bitmask = [bitmask] * n_channels
        mask = np.array(channel_bitmask, encoded_frame.dtype)
        mask = np.tile(mask, (*encoded_frame.shape[:-1], 1))
        masked_data = np.bitwise_and(encoded_frame, mask)
        # convert each element to binary string and take last `num_lsb` bits
        masked_data = masked_data.reshape((prod(masked_data.shape)))
        masked_data_str = [f"{i:08b}"[-num_lsb:] for i in masked_data]
        # concat all the binary strings and split by byte
        binary_data = "".join(masked_data_str)
        all_bytes = [binary_data[i: i+8]
                     for i in range(0, len(binary_data), 8)]
        # iterate over all bytes and convert from bits to characters sequentially
        # until the stop condition is reached
        for byte in all_bytes:
            self.decoded_data += chr(int(byte, 2))
            if early_stop is not None:
                if self.decoded_data[-len(early_stop):] == early_stop:
                    if not keep_early_stop:
                        self.decoded_data = self.decoded_data[:-
                                                              len(early_stop)]
                    break
        return self.decoded_data

    @abc.abstractmethod
    def read_file(
        self,
        filename: str
    ) -> (np.ndarray[Union[int, np.uint8, np.int16, np.int32]], NamedTuple):
        """Reads the file into a numpy array

        Args:
            filename (str): filepath to the file

        Returns:
            np.ndarray: file data as a numpy array

        Raises:
            FileNotFoundError: file not found
        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"File {filename} not found.")


class ImageDecoder(Decoder):
    """Image decoder class
    """

    def decode(
        self,
        encoded_data: np.ndarray[Union[int, np.uint8, np.int16, np.int32]],
        num_lsb: int = 1
    ) -> str:
        """Decodes the secret data from the image file

        Args:
            encoded_data (np.ndarray[Union[int, np.uint8, np.int16, np.int32]]): image data
            num_lsb (int, optional): number of LSBs to decode from. Defaults to 1.

        Returns:
            str: decoded secret data
        """
        self.decoded_data = super()._decode_frame(encoded_data, num_lsb)
        return self.decoded_data

    def read_file(
        self,
        filename: str
    ) -> (np.ndarray[Union[int, np.uint8, np.int16, np.int32]], NamedTuple):
        """Reads the image file into a numpy array

        Args:
            filename (str): filepath to the image file

        Returns:
            np.ndarray: image data as a numpy array

        Raises:
            FileNotFoundError: image file not found
        """
        super().read_file(filename)
        image = cv2.imread(filename)
        if image is None:
            raise IOError(f"File {filename} is not a valid image file.")
        return image, None


class AudioDecoder(Decoder):
    """Audio decoder class
    """

    def decode(
        self,
        encoded_data: np.ndarray[Union[int, np.uint8, np.int16, np.int32]],
        num_lsb: int = 1
    ) -> str:
        """Decodes the secret data from the audio file

        Args:
            encoded_data (np.ndarray[Union[int, np.uint8, np.int16, np.int32]]): audio data
            num_lsb (int, optional): number of LSBs to decode from. Defaults to 1.

        Returns:
            str: decoded secret data
        """
        self.decoded_data = super()._decode_frame(encoded_data, num_lsb)
        return self.decoded_data

    def read_file(
        self,
        filename: str
    ) -> (np.ndarray[Union[int, np.uint8, np.int16, np.int32]], NamedTuple):
        """Reads the audio file into a numpy array

        Args:
            filename (str): filepath to the audio file

        Raises:
            ValueError: invalid audio file format. Only .wav files are supported.

        Returns:
            np.ndarray[Union[int, np.uint8, np.int16, np.int32]]: audio data as a numpy array
        """
        super().read_file(filename)
        ext = os.path.splitext(filename)[1][1:]
        if ext not in util.AUDIO_EXTENSIONS:
            raise ValueError(
                f"Invalid audio file format. Only .wav files are supported.")
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


class VideoDecoder(Decoder):
    """Video decoder class
    """

    def decode(self, encoded_data, num_lsb) -> str:
        self.decoded_data = super()._decode_frame(encoded_data, num_lsb)
        return self.decoded_data

    def _batched_decode(
        self,
        encoded_data,
        num_lsb,
        batch_size=10,
        early_stop="====="
    ) -> str:
        """Decode the encoded video file in batches

        Args:
            encoded_data (np.ndarray): video frames
            num_lsb (int): number of LSBs to use for decoding
            batch_size (int, optional): number of video frames to decode at a time. Defaults to 10.

        Returns:
            str: encoded data
        """
        # raise NotImplementedError("Method not implemented.")
        decoded_data_all = ""
        num_equals = 0
        for i in range(0, encoded_data.shape[0], batch_size):
            decoded_data = self._decode_frame(
                encoded_data[i:i+batch_size], num_lsb, keep_early_stop=True)
            leading_num_equals = re.search(r"={1,5}", decoded_data[:5])
            if leading_num_equals is not None:
                leading_num_equals = len(leading_num_equals.group())
                if leading_num_equals + num_equals >= 5:
                    decoded_data_all = decoded_data_all[:-num_equals]
                    return decoded_data_all
            stop_location = decoded_data.find(early_stop)
            if stop_location != -1:
                return decoded_data_all + decoded_data[:stop_location]
            elif re.search(r"={1,4}", decoded_data[-4:]):
                # check if trailing characters are all '=
                num_equals = len(re.search(r"=", decoded_data[-5:]).group())
                decoded_data_all += decoded_data[:-num_equals]
        return decoded_data_all

    def read_file(
        self,
        filename: str
    ) -> (np.ndarray[Union[int, np.uint8, np.int16, np.int32]], NamedTuple):
        """Reads the video file into a numpy array

        Args:
            filename (str): filepath to the video file

        Returns:
            np.ndarray[Union[int, np.uint8, np.int16, np.int32]]: video data as a numpy array
        """
        super().read_file(filename)
        video = cv2.VideoCapture(filename)
        params = namedtuple("VideoParams", ["fps", "width", "height"])(video.get(
            cv2.CAP_PROP_FPS), video.get(cv2.CAP_PROP_FRAME_WIDTH), video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_data = []
        while video.isOpened():
            ret, frame = video.read()
            if ret:
                video_data.append(frame)
            else:
                break
        video_data = np.array(video_data)
        return video_data, params
