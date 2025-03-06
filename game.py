import pygame
from ui import UI

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.ui = UI(screen)
        self._entities = pygame.sprite.Group()

    def add(self, entity):
        self._entities.add(entity)
       
    @property
    def name(self):
        pass

    def update(self):
        [e.update() for e in self._entities]
        self._entities.draw(self.screen)
        self.ui.update()