import pytest
import wave

import cv2

from steganography.decoder import ImageDecoder, AudioDecoder, VideoDecoder
from steganography.encoder import ImageEncoder, AudioEncoder, VideoEncoder

class TestEncodeDecode:
    input_str = "Hello, World!"

    @pytest.fixture
    def image(self):
        image_file = "tests/black_128.png"
        image = cv2.imread(image_file)
        return [ImageEncoder(), ImageDecoder(), image]

    @pytest.fixture
    def audio(self):
        audio_file = "tests/test.wav"
        audio = wave.open(audio_file, mode="rb")
        return [AudioEncoder(), AudioDecoder(), audio]
    
    @pytest.fixture
    def video(self):
        video_file = "tests/test.mp4"
        video = cv2.VideoCapture(video_file)
        return [VideoEncoder(), VideoDecoder(), video]
    
    @pytest.fixture
    def lsb(self):
        return list(range(1, 9))

    def test_encoder_decoder(self, audio, image, video, lsb):
        for encoder, decoder, cover_file in [image, audio, video]:
            for num_lsb in lsb:
                encoded_data = encoder.encode(cover_file, TestEncodeDecode.input_str, num_lsb)
                decoded_str = decoder.decode(encoded_data, num_lsb)
                assert TestEncodeDecode.input_str == decoded_str
