import os
import pytest
import wave

import numpy as np
import cv2

from steganography.decoder import ImageDecoder, AudioDecoder, VideoDecoder
from steganography.encoder import ImageEncoder, AudioEncoder, VideoEncoder

class TestEncodeDecode:
    input_str = "Hello, World!"

    @pytest.fixture
    def image(self):
        image_file = "tests/black_128.png"
        return [ImageEncoder(), ImageDecoder(), image_file]

    @pytest.fixture
    def audio(self):
        audio_file = "tests/test.wav"
        return [AudioEncoder(), AudioDecoder(), audio_file]
    
    @pytest.fixture
    def video(self):
        video_file = "tests/test.mp4"
        return [VideoEncoder(), VideoDecoder(), video_file]
    
    @pytest.fixture
    def lsb(self):
        return list(range(1, 9))

    def test_encoder_decoder(self, audio, image, video, lsb):
        for encoder, decoder, cover_filename in [image, audio, video]:
            cover_file, params = encoder.read_file(cover_filename)
            for num_lsb in lsb:
                encoded_data = encoder.encode(cover_file, TestEncodeDecode.input_str, num_lsb)
                decoded_str = decoder.decode(encoded_data, num_lsb)
                assert TestEncodeDecode.input_str == decoded_str

    def test_file_integrity(self, audio, image, video, lsb):
        for encoder, decoder, cover_filename in [image, audio, video]:
            cover_file, params = encoder.read_file(cover_filename)
            ext = ""
            match encoder:
                case ImageEncoder():
                    ext = "png"
                case AudioEncoder():
                    ext = "wav"
                case VideoEncoder():
                    ext = "mov"
                case _:
                    raise NotImplementedError("Method not implemented.")
            output_temp_filename = f"tests/output.{ext}"
            for num_lsb in lsb:
                encoded_data = encoder.encode(cover_file, TestEncodeDecode.input_str, num_lsb)
                encoder.write_file(encoded_data, output_temp_filename, params)
                encoded_read_data = decoder.read_file(output_temp_filename)
                decoded_str = decoder.decode(encoded_read_data, num_lsb)
                os.remove(output_temp_filename)
                assert TestEncodeDecode.input_str == decoded_str
