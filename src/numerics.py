import numpy as np
import scipy as sp

from src.physics import SPEED_OF_SOUND, Space

dt = 1 / 24_000
alpha = SPEED_OF_SOUND
h = 1 / 25
tau = ((dt * alpha) / h) ** 2

tau = 0.25
print("Startet Simulation with tau=", tau)

LaplaceOperator = np.array([
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

    def __init__(self, room: Space):
        self.time_steps_needed = LaplaceOperator.shape[0]
        self.data = np.zeros((self.time_steps_needed, *room.dimensions))

    def update(self):
        self._move_data_in_time()  # initialize next time step
        #for time_step in range(1, self.time_steps_needed):  # skip 0, we only care about past time steps
        #    self.data[0] += sp.signal.convolve(self.data[time_step], LaplaceOperator[time_step], mode="same",
        #                                       method="direct")
        u = self.data
        dimx = self.data.shape[1]
        dimy = self.data.shape[2]
        u[0, 1:dimx-1, 1:dimy-1] = 0.25 * (u[1, 0:dimx-2, 1:dimy-1] +
                                           u[1, 2:dimx,   1:dimy-1] +
                                           u[1, 1:dimx-1, 0:dimy-2] +
                                           u[1, 1:dimx-1, 2:dimy] - 4*u[1, 1:dimx-1, 1:dimy-1]) \
                                   + 2 * u[1, 1:dimx-1, 1:dimy-1] - u[2, 1:dimx-1, 1:dimy-1]
        #self.data[abs(self.data) < self.THRESHOLD] = 0
        self._reduce_power()

    def _move_data_in_time(self):
        """
        shifts data from t to t+1
        """
        self.data[2] = self.data[1]
        self.data[1] = self.data[0]
        return
        for time_step in range(self.time_steps_needed - 1, 0, -1):
            self.data[time_step] = self.data[time_step - 1]
        self.data[0] = 0

    def _reduce_power(self):
        self.data[0,:,:] *= 0.995
