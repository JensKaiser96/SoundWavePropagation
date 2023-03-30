import pygame
import time

from src.io import str_to_safe_path
from src.numerics import Simulation
from src.utils import float_to_3x_uint8, binary_to_3x_unit8


class Colors:
    BLACK = (0, 0, 0)


class LiveSimulationView:
    def __init__(self, sim: Simulation, scale=2, fps=25):
        self.sim = sim
        self.scale = scale
        pygame.init()
        self.display = pygame.display.set_mode(self.sim.room.dimensions * scale)
        pygame.display.set_caption("Sound Wave Propagation Simulation")
        self.font = pygame.font.SysFont(None, 24)

        self.last_update = 0
        self.fps = fps  # time in ms per frame

    def draw_now(self):
        if pygame.QUIT in pygame.event.get():
            pygame.quit()
            return RuntimeError("quit game")
        if self.fps == 0:
            return True
        now = round(time.time() * 1000)
        return now > self.last_update + 1000/self.fps

    def draw(self):
        self._draw_data()
        self._draw_borders()
        self._draw_obstacles()
        self._draw_in_signals()
        self._draw_out_signals()
        self._draw_tick()
        self.last_update = round(time.time() * 1000)
        pygame.display.update()

    def _draw_data(self):
        pixels = float_to_3x_uint8(self.sim.data_now)
        surface = pygame.surfarray.make_surface(pixels)
        self._draw_surface(surface)

    def _draw_tick(self):
        img = self.font.render(f"tick: {self.sim.tick}", True, Colors.BLACK)
        self.display.blit(img, (0, 0))

    def _draw_in_signals(self):
        for in_signal in self.sim.input_signals:
            pygame.draw.circle(self.display, Colors.BLACK, in_signal.signal.position * self.scale + 1, 3, 1)

    def _draw_out_signals(self):
        for out_signal in self.sim.output_signals:
            pygame.draw.circle(self.display, Colors.BLACK, out_signal.signal_ch1.position * self.scale + 1, 3, 0)
            if out_signal.stereo:
                pygame.draw.circle(self.display, Colors.BLACK, out_signal.signal_ch2.position * self.scale + 1, 3, 0)

    def _draw_borders(self):
        if not self.sim.open_borders:
            pygame.draw.rect(self.display, Colors.BLACK, ((0, 0), self.sim.room.dimensions*self.scale), 1)

    def _draw_obstacles(self):
        pixels = binary_to_3x_unit8(self.sim.obstacles)
        surface = pygame.surfarray.make_surface(pixels)
        self._draw_surface(surface)

    def _draw_surface(self, surface):
        self.display.blit(
            pygame.transform.scale(surface, self.sim.room.dimensions * self.scale),
            (0, 0)
        )

    def screenshot(self, filepath: str):
        path = str_to_safe_path(filepath, ".jpeg")
        pygame.image.save(self.display, path)
