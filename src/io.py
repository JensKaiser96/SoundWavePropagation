import datetime
from PIL import Image
import imageio as iio
import numpy as np
from pathlib import Path

from scipy.io import wavfile
from src.utils import clip_values, float_to_3x_uint8


STANDARD_FPS = 30


def to_jpeg(data: np.ndarray, filepath: str):
    suffix = ".jpeg"
    path = str_to_safe_path(filepath, suffix)
    im = Image.fromarray(float_to_3x_uint8(data))
    im.save(path)


def to_gif(filepath: str, data: np.ndarray, fps=STANDARD_FPS):
    suffix = ".gif"
    path = str_to_safe_path(filepath, suffix)
    iio.mimsave(path, clip_values(data), format='GIF-PIL', fps=fps, loop=100)


def to_mp4(filepath: str, data: np.ndarray):
    suffix = ".mp4"
    path = str_to_safe_path(filepath, suffix)
    writer = iio.get_writer(path, fps=20)

    for frame in clip_values(data):
        writer.append_data(frame)
    writer.close()


def to_wav(filepath: str, sr: int, data: np.ndarray):
    suffix = ".wav"
    path = str_to_safe_path(filepath, suffix)
    wavfile.write(path, sr, data)


def read_wav(filepath: str) -> (int, np.ndarray):
    return wavfile.read(filepath)


def str_to_safe_path(filepath: str, suffix):
    if filepath[0] != ".":
        filepath = "./" + filepath
    path = Path(filepath)
    path = path.with_suffix(suffix)
    parent = path.parent
    parent.mkdir(exist_ok=True, parents=True)
    if path.is_file():
        time_stamp = datetime.datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")
        path = path.with_stem(f"{path.stem}_{time_stamp}")
    return path
