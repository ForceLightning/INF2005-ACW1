import os
import sys

import abc
import io
from typing import Union
import wave
from math import prod

import numpy as np
import PIL
import cv2

from steganography.util import _data_to_binstr, _data_to_binarray


class Decoder(abc.ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def decode(self, encoded_data, num_lsb) -> str:
        raise NotImplementedError("Method not implemented.")

    def _decode_frame(self, encoded_frame, num_lsb):
        binary_data = ""
        bit_depth = encoded_frame.dtype.itemsize * 8
        if num_lsb > bit_depth or num_lsb < 1:
            raise ValueError(
                "num_lsb must be between 1 and {}".format(bit_depth))
        bitmask = 2 ** num_lsb - 1
        n_frames = encoded_frame.shape[0]
        n_channels = encoded_frame.shape[-1]
        channel_bitmask = [bitmask] * n_channels
        mask = np.array(channel_bitmask, encoded_frame.dtype)
        mask = np.tile(mask, (*encoded_frame.shape[:-1] , 1))
        masked_data = np.bitwise_and(encoded_frame, mask)
        # convert each element to binary string and take last `num_lsb` bits
        masked_data = masked_data.reshape((prod(masked_data.shape)))
        masked_data_str = [f"{i:08b}"[-num_lsb:] for i in masked_data]
        # concat all the binary strings and split by byte
        binary_data = "".join(masked_data_str)
        all_bytes = [binary_data[i: i+8]
                     for i in range(0, len(binary_data), 8)]
        decoded_data = ""
        # iterate over all bytes and convert from bits to characters sequentially
        # until the stop condition is reached
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "=====":
                decoded_data = decoded_data[:-5]
                break
        return decoded_data


class ImageDecoder(Decoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def decode(self, encoded_data, num_lsb) -> str:
        return super()._decode_frame(encoded_data, num_lsb)

class AudioDecoder(Decoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def decode(self, encoded_data, num_lsb) -> str:
        return super()._decode_frame(encoded_data, num_lsb)


class VideoDecoder(Decoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def decode(self, encoded_data, num_lsb) -> str:
        raise NotImplementedError("Method not implemented.")
