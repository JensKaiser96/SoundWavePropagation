import numpy as np


def clip_values(data: np.ndarray) -> np.ndarray:
    return np.clip(data + 128, 0, 255)


def binary_to_3x_unit8(data: np.ndarray):
    result = np.zeros((*data.shape, 3), dtype=np.uint8)
    result[:, :, 0] = data * 255
    result[:, :, 1] = data * 255
    result[:, :, 2] = data * 255
    return result


def float_to_3x_uint8(data: np.ndarray) -> np.ndarray:
    """
    =0: white
    >0: red
    <0: blue
             -    0     +
    RED      0   255   255
    GREEN    0   255    0
    BLUE    255  255    0
    """
    result = np.zeros((*data.shape, 3), dtype=np.uint8)
    result[:, :, 0] = np.clip(data, -255, 0) + 255  # red
    result[:, :, 1] = (np.abs(np.clip(data, -255, 255)) - 255) * -1  # green
    result[:, :, 2] = (np.clip(data, 0, 255) - 255) * -1   # blue
    return result
