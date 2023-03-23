import numpy as np
import pygame
import time
from src.physics import Space
from src.utils import clip_values


class Window:
    def __init__(self, room: Space, scale=1, fps=25):
        self.room = room
        self.scale = scale
        pygame.init()
        self.display = pygame.display.set_mode((room.dimensions.x * scale, room.dimensions.y * scale))
        pygame.display.set_caption("Sound Wave Propagation Simulation")

        self.last_update = 0
        self.delta_s = 1000/fps  # time in ms per frame

    def update(self, data):
        pixels = np.zeros((*self.room.dimensions, 3), dtype=np.uint8)
        pixels[:,:,0] = clip_values(data)
        pixels[:,:,1] = clip_values(data)
        pixels[:,:,2] = clip_values(data)

        surface = pygame.surfarray.make_surface(pixels)
        self.display.blit(pygame.transform.scale(surface, (300*2, 300*2)), (0, 0))
        self.last_update = round(time.time() * 1000)
        pygame.display.update()

    def draw_now(self):
        if pygame.QUIT in pygame.event.get():
            pygame.quit()
            return RuntimeError("quit game")
        now = round(time.time() * 1000)
        return now > self.last_update + self.delta_s
