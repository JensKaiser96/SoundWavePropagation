import datetime
import imageio as iio
import numpy as np
from pathlib import Path

from src.utils import clip_values


STANDARD_FPS = 30


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


def str_to_safe_path(filepath: str, suffix):
    path = Path(filepath)
    path.with_suffix(suffix)
    parent = path.parent
    parent.mkdir(exist_ok=True)
    if path.is_file():
        time_stamp = datetime.datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")
        path.with_stem(f"{path.stem}_{time_stamp}")
    return path
