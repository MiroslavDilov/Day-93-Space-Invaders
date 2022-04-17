import pygame
from main import App


class Spaceship(App):
    def __init__(self):
        self.rect = pygame.Rect(50, 50, 50, 50)

    def on_loop(self):
        pygame.draw.rect(self.window, (255,0,0), self.rect)