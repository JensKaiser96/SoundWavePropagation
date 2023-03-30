import numpy as np
import scipy as sp

from src.physics import SPEED_OF_SOUND, Space
from src.signals import InputSignal, OutputSignal


def laplace_operator(tau):
    return np.array([
        np.zeros((3, 3)),  # t0
        # t-1
        tau * np.array(
            [[0, 1, 0],
             [1, -4, 1],
             [0, 1, 0]])
        + np.array(
            [[0, 0, 0],
             [0, 2, 0],
             [0, 0, 0]]),
        # t-2
        np.array(
            [[0, 0, 0],
             [0, -1, 0],
             [0, 0, 0]])
    ])


class Simulation:
    THRESHOLD = 0.01
    idt = 24_000
    ih = 25

    def __init__(self, room: Space, idt=idt, ih=ih,
                 input_signals: list[InputSignal] = None,
                 output_signals: list[OutputSignal] = None,
                 open_borders=False,
                 obstacles: np.ndarray = None):
        self.room = room
        self.idt = idt
        self.ih = ih
        self.LaplaceOperator = laplace_operator(self.tau)
        self.time_steps_needed = self.LaplaceOperator.shape[0]
        self.data = np.zeros((self.time_steps_needed, *room.dimensions))
        self.open_borders = open_borders
        self.obstacles = obstacles

        if input_signals is None:
            input_signals = []
        self.input_signals = input_signals
        if output_signals is None:
            output_signals = []
        self.output_signals = output_signals

        self.tick = 0

    @property
    def tau(self):
        alpha = SPEED_OF_SOUND
        dt = 1 / self.idt
        h = 1 / self.ih
        tau = ((dt * alpha) / h) ** 2
        return tau

    @property
    def kappa(self):
        return SPEED_OF_SOUND * (self.ih / self.idt)

    @property
    def kappa_fraction(self):
        return (self.kappa - 1)/(self.kappa + 1)

    @property
    def data_now(self):
        return self.data[0]

    def update(self):
        self._set_input_signals()
        self._move_data_in_time()  # initialize next time step
        for time_step in range(1, self.time_steps_needed):  # skip 0, we only care about past time steps
            self.data[0] += sp.signal.convolve(self.data[time_step], self.LaplaceOperator[time_step], mode="same",
                                               method="direct")  # fft, auto
        self.set_border_conditions()
        self.calculate_obstacle_collision()
        self._reduce_power()
        self._get_output_signals()
        self.tick += 1

    def set_border_conditions(self):
        if not self.open_borders:
            return
        N = self.room.dimensions.y-1
        M = self.room.dimensions.x-1
        # top
        self.data[0, 0, :] = self.data[1, 1, :] + self.kappa_fraction * (self.data[0, 1, :] - self.data[1, 0, :])
        # bottom
        self.data[0, M, :] = self.data[1, M-1, :] + self.kappa_fraction * (self.data[0, M-1, :] - self.data[1, M, :])
        # left
        self.data[0, :, 0] = self.data[1, :, 1] + self.kappa_fraction * (self.data[0, :, 1] - self.data[1, :, 0])
        # right
        self.data[0, :, N] = self.data[1, :, N-1] + self.kappa_fraction * (self.data[0, :, N-1] - self.data[1, 1, N])

    def _set_input_signals(self):
        for input_signal in self.input_signals:
            input_signal.set(self.data_now, self.tick)

    def _get_output_signals(self):
        for output_signal in self.output_signals:
            output_signal.get(self.data_now)

    @property
    def all_inputs_done(self) -> bool:
        return all([in_signal.done for in_signal in self.input_signals])

    def save_all_output_signals(self, filepath: str):
        for i, output_signal in enumerate(self.output_signals):
            output_signal.save_recording(f"{filepath}_{i}")

    def _move_data_in_time(self):
        """
        shifts data from t to t+1
        """
        for time_step in range(self.time_steps_needed - 1, 0, -1):
            self.data[time_step] = self.data[time_step - 1]
        self.data[0] = 0

    def _reduce_power(self):
        self.data[0, :, :] *= 0.995

    def calculate_obstacle_collision(self):
        if self.obstacles is None:
            return
        self.data[0, :, :] *= self.obstacles


class Border:
    TOP = "Border.Top"
    BOTTOM = "Border.Bottom"
    LEFT = "Border.Left"
    RIGHT = "Border.Right"

    def __init__(self, data: np.ndarray, kappa: float):
        self.data = data
        self.height = data.shape[1]
        self.width = data.shape[2]
        self.kappa = kappa
        self.kappa_frac = (self.kappa - 1)/(self.kappa + 1)

    def set_borders(self, side: str):
        N = self.height
        M = self.width
        if side == self.TOP:
            self.data[0, 0, :] = self.data[1, 1, :] + self.kappa_frac * (self.data[0, 1, :] - self.data[1, 0, :])
        if side == self.BOTTOM:
            self.data[0, M, :] = self.data[1, M-1, :] + self.kappa_frac * (self.data[0, M-1, :] - self.data[1, M, :])
        if side == self.LEFT:
            self.data[0, :, 0] = self.data[1, :, 1] + self.kappa_frac * (self.data[0, :, 1] - self.data[1, :, 0])
        if side == self.RIGHT:
            self.data[0, :, N] = self.data[1, :, N-1] + self.kappa_frac * (self.data[0, :, N-1] - self.data[1, 1, N])
