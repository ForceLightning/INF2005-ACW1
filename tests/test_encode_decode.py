import os
import pytest
import wave

import numpy as np
import cv2

from steganography.decoder import ImageDecoder, AudioDecoder, VideoDecoder
from steganography.encoder import ImageEncoder, AudioEncoder, VideoEncoder


class TestEncodeDecode:
    input_str = """[Verse 1]
There once was a ship that put to sea
The name of the ship was the Billy of Tea
The winds blew up, her bow dipped down
O blow, my bully boys, blow (Huh!)

[Chorus]
Soon may the Wellerman come
To bring us sugar and tea and rum
One day, when the tonguin' is done
We'll take our leave and go

[Verse 2]
She had not been two weeks from shore
When down on her, a right whale bore
The captain called all hands and swore
He'd take that whale in tow (Huh!)

[Chorus]
Soon may the Wellerman come
To bring us sugar and tea and rum
One day, when the tonguin' is done
We'll take our leave and go

[Verse 3]
Before the boat had hit the water
The whale's tail came up and caught her
All hands to the side, harpooned and fought her
When she dived down low (Huh!)
[Chorus]
Soon may the Wellerman come
To bring us sugar and tea and rum
One day, when the tonguin' is done
We'll take our leave and go

[Verse 4]
No line was cut, no whale was freed
The Captain's mind was not of greed
But he belonged to the Wellerman's creed
She took that ship in tow (Huh!)

[Chorus]
Soon may the Wellerman come
To bring us sugar and tea and rum
One day, when the tonguin' is done
We'll take our leave and go

[Verse 5]
For forty days, or even more
The line went slack, then tight once more
All boats were lost, there were only four
But still that whale did go (Huh!)

[Chorus]
Soon may the Wellerman come
To bring us sugar and tea and rum
One day, when the tonguin' is done
We'll take our leave and go
[Verse 6]
As far as I've heard, the fight's still on
The line's not cut and the whale's not gone
The Wellerman makes his regular call
To encourage the Captain, crew, and all (Huh!)

[Chorus]
Soon may the Wellerman come
To bring us sugar and tea and rum
One day, when the tonguin' is done
We'll take our leave and go (Huh!)
Soon may the Wellerman come
To bring us sugar and tea and rum
One day, when the tonguin' is done
We'll take our leave and go"""

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
        return list(range(5, 9))

    def test_encoder_decoder(self, audio, image, video, lsb):
        for encoder, decoder, cover_filename in [image, audio, video]:
            cover_file, params = encoder.read_file(cover_filename)
            for num_lsb in lsb:
                encoded_data = encoder.encode(
                    cover_file, TestEncodeDecode.input_str, num_lsb)
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
                    ext = "avi"
                case _:
                    raise NotImplementedError("Method not implemented.")
            output_temp_filename = f"tests/output.{ext}"
            if os.path.isfile(output_temp_filename):
                os.remove(output_temp_filename)
            for num_lsb in lsb:
                encoded_data = encoder.encode(
                    cover_file, TestEncodeDecode.input_str, num_lsb)
                encoder.write_file(encoded_data, output_temp_filename, params)
                encoded_read_data, read_data_params = decoder.read_file(
                    output_temp_filename)
                assert params == read_data_params
                decoded_str = decoder.decode(encoded_read_data, num_lsb)
                assert TestEncodeDecode.input_str == decoded_str
                os.remove(output_temp_filename)

    def test_file_similarity(self, video, lsb):
        encoder, decoder, cover_filename = video
        cover_file, params = encoder.read_file(cover_filename)
        ext = "avi"
        output_temp_filename = f"tests/output.{ext}"
        if os.path.isfile(output_temp_filename):
            os.remove(output_temp_filename)
        for num_lsb in lsb:
            encoded_data = encoder.encode(
                cover_file, TestEncodeDecode.input_str, num_lsb)
            encoder.write_file(encoded_data, output_temp_filename, params)
            encoded_read_data, read_data_params = decoder.read_file(
                output_temp_filename)
            assert params == read_data_params
            assert np.allclose(encoded_data, encoded_read_data)
            decoded_str = decoder.decode(encoded_read_data, num_lsb)
            assert TestEncodeDecode.input_str == decoded_str
            os.remove(output_temp_filename)