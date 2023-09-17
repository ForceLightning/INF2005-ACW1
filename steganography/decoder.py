import os
import sys

import abc
import io
from typing import Union
import wave

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

class ImageDecoder(Decoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def decode(self, encoded_data, num_lsb) -> str:
        binary_data = ""
        subpixel_mask = 2 ** num_lsb - 1
        h, w, c = encoded_data.shape
        channel_bitmask = [subpixel_mask] * c
        mask = np.array(channel_bitmask, np.uint8)
        mask = np.tile(mask, (h, w, 1))
        masked_data = np.bitwise_and(encoded_data, mask)
        # convert each element to binary string and take last `num_lsb` bits
        masked_data = masked_data.reshape((h * w * c))
        masked_data_str = [f"{i:08b}"[-num_lsb:] for i in masked_data]
        # concatenate all the binary strings
        binary_data = "".join(masked_data_str)
        # split by 8-bits
        all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
        # convert from bits to characters sequentially until the stop condition is reached
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "=====":
                decoded_data = decoded_data[:-5]
                break
        return decoded_data

class AudioDecoder(Decoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def decode(self, encoded_data, num_lsb) -> str:
        raise NotImplementedError("Method not implemented.")

class VideoDecoder(Decoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def decode(self, encoded_data, num_lsb) -> str:
        raise NotImplementedError("Method not implemented.")