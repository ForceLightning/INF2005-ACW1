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

class Encoder(abc.ABC):
    def __init__(self, *args, **kwargs):
        pass
    
    @abc.abstractmethod
    def encode(self, cover_file_bytes, secret_data) -> Image.Image:
        raise NotImplementedError("Method not implemented.")
        bin_encoded_data = self._data_to_binstr(secret_data)

    def __call__(self, *args, **kwargs):
        return self.encode(*args, **kwargs)

    def _data_to_binstr(self, data: Union[str, bytes, np.ndarray, int]) -> str:
        match data:
            case isinstance(data, str):
                return ''.join([f"{ord(i):08b}" for i in data])
            case isinstance(data, int):
                return f"{data:08b}"
            case isinstance(data, bytes):
                return [f"{i:08b}" for i in data]
            case isinstance(data, np.ndarray):
                return [f"{i:08b}" for i in data]
            case _:
                raise TypeError(f"data of type {type(data)} not supported.")

class ImageEncoder(Encoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def encode(self, cover_file_bytes, secret_data) -> Image.Image:
        raise NotImplementedError("Method not implemented.")
    
class AudioEncoder(Encoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def encode(self, cover_file_bytes, secret_data) -> Image.Image:
        raise NotImplementedError("Method not implemented.")
    
class VideoEncoder(Encoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def encode(self, cover_file_bytes, secret_data) -> Image.Image:
        raise NotImplementedError("Method not implemented.")