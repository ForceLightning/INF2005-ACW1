import pytest

from steganography.decoder import ImageDecoder, AudioDecoder, VideoDecoder
from steganography.encoder import ImageEncoder, AudioEncoder, VideoEncoder

class TestEncodeDecode:
    input_str = "Hello, World!"

    @pytest.fixture
    def audio(self):
        audio_file = "tests/test.wav"
        return [AudioEncoder, AudioDecoder, audio_file]

    @pytest.fixture
    def image(self):
        image_file = "tests/sit-logo-primary.png"
        return [ImageEncoder, ImageDecoder, image_file]
    
    @pytest.fixture
    def video(self):
        video_file = "tests/test.mp4"
        return [VideoEncoder, VideoDecoder, video_file]

    def test_encoder_decoder(self, audio, image, video):
        for encoder, decoder, cover_filename in [audio, image, video]:
            encoder = encoder()
            decoder = decoder()
            
            encoded_data = encoder.encode(cover_filename, TestEncodeDecode.input_str)
            decoded_str = decoder.decode(encoded_data)
            assert TestEncodeDecode.input_str == decoded_str
