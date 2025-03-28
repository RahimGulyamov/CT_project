import pygame
from src.back.Config import *


class Window:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(CAPTION)
        self.display = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]))

    def GetDisplay(self):
        return self.display
