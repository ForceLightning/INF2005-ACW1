import os
import sys

import abc
import io
from typing import Union
import wave

import PIL
import cv2

class Decoder(abc.ABC):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs) -> str:
        return self.decode(*args, **kwargs)

    @abc.abstractmethod
    def decode(self, encoded_data) -> str:
        raise NotImplementedError("Method not implemented.")

class ImageDecoder(Decoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def decode(self, encoded_data):
        raise NotImplementedError("Method not implemented.")

class AudioDecoder(Decoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def decode(self, encoded_data):
        raise NotImplementedError("Method not implemented.")

class VideoDecoder(Decoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def decode(self, encoded_data):
        raise NotImplementedError("Method not implemented.")