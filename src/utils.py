import numpy as np


def clip_values(data: np.ndarray) -> np.ndarray:
    return np.clip(data + 128, 0, 255)
