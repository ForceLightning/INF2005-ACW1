import os
import sys

import abc
import io
from typing import Union
import wave

import PIL
from PIL import Image
import cv2
import numpy as np

from steganography.util import _data_to_binstr, _data_to_binarray

class Encoder(abc.ABC):
    def __init__(self, *args, **kwargs):
        pass
    
    @abc.abstractmethod
    def encode(self, cover_file_bytes, secret_data, num_lsb):
        raise NotImplementedError("Method not implemented.")
        bin_encoded_data = self._data_to_binstr(secret_data)

class ImageEncoder(Encoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def encode(self, cover_file_bytes, secret_data, num_lsb):
        # raise NotImplementedError("Method not implemented.")
        stop_condition = "====="
        secret_data += stop_condition
        n_bytes = cover_file_bytes.shape[0] * cover_file_bytes.shape[1] * cover_file_bytes.shape[2]
        data_index = 0
        binary_secret_data = _data_to_binarray(secret_data, num_lsb)
        binary_secret_and_mask = np.bitwise_or(255 - (2 ** num_lsb - 1), binary_secret_data)
        data_len = len(binary_secret_data)
        if data_len > n_bytes:
            raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
        padding = n_bytes - data_len
        # padded values should be 255
        binary_secret_and_mask = np.pad(binary_secret_and_mask, (0, padding), constant_values=255)
        binary_secret_and_mask = binary_secret_and_mask.reshape(*cover_file_bytes.shape) # reshape to the shape of the cover file
        binary_secret_data = np.pad(binary_secret_data, (0, padding), constant_values=0)
        binary_secret_data = binary_secret_data.reshape(*cover_file_bytes.shape)
        # encode data into image with the bitwise operations A + (A * B)
        and_op = np.bitwise_and(cover_file_bytes, binary_secret_and_mask)
        or_op = np.bitwise_or(and_op, binary_secret_data)
        return or_op
        
class AudioEncoder(Encoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def encode(self, cover_file_bytes, secret_data, num_lsb):
        raise NotImplementedError("Method not implemented.")
    
class VideoEncoder(Encoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def encode(self, cover_file_bytes, secret_data, num_lsb):
        raise NotImplementedError("Method not implemented.")