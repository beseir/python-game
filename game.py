import pygame
from ui import UI
from scene import Scene
from camera import Camera

class Game(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.ui = UI(screen)
        self._entities = pygame.sprite.Group()
        self.camera = Camera((0, 0), screen.get_size())

    def add(self, entity):
        self._entities.add(entity)
    
    name = "Game"

    def update(self, events: list[pygame.event]) -> bool:
        shouldContinue = super().update(events)

        [e.update() for e in self._entities]

        self.camera.draw_group(self._entities, self.screen)
        self.ui.update()
        
        return shouldContinue

