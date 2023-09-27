from typing import Union

import numpy as np

def _data_to_binstr(data: Union[str, bytes, np.ndarray, int]) -> str:
    match data:
        case str():
            return ''.join([f"{ord(i):08b}" for i in data])
        case int() | np.uint8():
            return f"{data:08b}"
        case bytes() | np.ndarray():
            return [f"{i:08b}" for i in data]
        case _:
            raise TypeError(f"data of type {type(data)} not supported.")

def _data_to_binarray(data: Union[str, bytes, np.ndarray, int], num_lsb=1) -> np.ndarray:
    match data:
        case str():
            bin_str = ''.join([f"{ord(i):08b}" for i in data])
            int_vals = [int(i) for i in bin_str]
            padding = (num_lsb - (len(int_vals) % num_lsb)) % num_lsb
            int_vals += [0] * padding
            int_vals = [int_vals[i: i+num_lsb] for i in range(0, len(int_vals), num_lsb)] # split into groups of `num_lsb` bits
            # convert groups of `num_lsb` bits into a single integer per group
            int_vals = [int("".join([str(bit) for bit in bit_group]), 2) for bit_group in int_vals]
            return np.array(int_vals, np.uint8)
        case int() | np.uint8():
            return np.array([data], np.uint8)
        case bytes() | np.ndarray():
            return np.array(data, np.uint8)
        case _:
            raise TypeError(f"data of type {type(data)} not supported.")    

IMAGE_EXTENSIONS = ["bmp", "dib", "jpeg", "jpg", "jpe", "jp2", "png", "webp", "avif", "pbm", "pgm", "ppm", "sr", "ras", "tiff", "tif", "exr", "hdr", "pic"]
# AUDIO_EXTENSIONS = ["wav", "mp3", "ogg", "flac", "wma", "m4a", "aiff", "aac", "alac", "pcm", "dsd", "mp2", "amr", "ape", "au", "awb", "dct", "dss", "dvf", "gsm", "iklax", "ivs", "m4p", "mmf", "mpc", "msv", "nmf", "nsf", "ra", "raw", "tta", "voc", "vox", "wv", "8svx"]
AUDIO_EXTENSIONS = ["wav"]
VIDEO_EXTENSIONS = ["avi", "mov", "mp4", "mkv", "webm", "flv", "vob", "ogv", "ogg", "drc", "gifv", "mng", "qt", "wmv", "yuv", "rm", "rmvb", "asf", "amv", "mpg", "mp2", "mpeg", "mpe", "mpv", "m2v", "svi", "3gp", "3g2", "mxf", "roq", "nsv", "flv", "f4v", "f4p", "f4a", "f4b"]