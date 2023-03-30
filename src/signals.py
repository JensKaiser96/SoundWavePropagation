import numpy as np
from src.physics import Point2D
from src.io import read_wav, to_wav


class WAVSignal:
    sr = 24_000

    def __init__(self, position: Point2D, data: np.ndarray = None, sr=sr):
        self.position = position
        self.data = data
        self.sr = sr

    def load(self, filepath: str):
        self.sr, self.data = read_wav(filepath)
        return self

    def save(self, filepath: str):
        to_wav(filepath, self.sr, self.data)

    def move_to(self, new_position: Point2D):
        self.position = new_position


class InputSignal:
    def __init__(self, position: Point2D, data: np.ndarray | None):
        self.signal = WAVSignal(position, data)
        self.done = False

    def set(self, out_data: np.ndarray, tick: int):
        if self.done:
            return
        try:
            out_data[self.signal.position.y, self.signal.position.x] = self.signal.data[tick]
        except IndexError:
            self.done = True

    @staticmethod
    def from_wav(position: Point2D, filepath: str):
        in_signal = InputSignal(position, None)
        in_signal.signal.load(filepath)
        return in_signal


class OutputSignal:
    stereo = False

    def __init__(self, position_ch1: Point2D, position_ch2: Point2D = None):
        self.signal_ch1 = WAVSignal(position_ch1)
        self.data_ch1 = []
        if position_ch2 is not None:
            self.stereo = True
            self.signal_ch2 = WAVSignal(position_ch2)
            self.data_ch2 = []

    def get(self, in_data: np.ndarray):
        self.data_ch1.append(in_data[self.signal_ch1.position.y, self.signal_ch1.position.x])
        if self.stereo:
            self.data_ch2.append(in_data[self.signal_ch2.position.y, self.signal_ch2.position.x])

    @property
    def sr(self):
        if not self.stereo:
            return self.signal_ch1.sr
        sr_ch1 = self.signal_ch1.sr
        sr_ch2 = self.signal_ch2.sr
        if sr_ch1 != sr_ch2:
            raise RuntimeError(f"Sampling rate of both signals must be equal. {sr_ch1=}, {sr_ch2=}")
        return sr_ch1

    def stop_recording(self):
        self.signal_ch1.data = np.array(self.data_ch1)
        if self.stereo:
            self.signal_ch2.data = np.array(self.data_ch2)

    def save_recording(self, filepath):
        self.stop_recording()
        if not self.stereo:
            to_wav(filepath, self.sr, self.signal_ch1.data)
            return self
        to_wav(filepath, self.sr, np.array([self.signal_ch1.data, self.signal_ch2.data]))
