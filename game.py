import pygame
from scene import Scene

class Game(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self._entities = pygame.sprite.Group()

    def add(self, entity):
        self._entities.add(entity)
    
    name = "Game"

    def update(self, events: list[pygame.event]) -> bool:
        shouldContinue = super().update(events)

        [e.update() for e in self.entities]

        return shouldContinue
