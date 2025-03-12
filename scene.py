import pygame

class Scene:
    def __init__(self, screen):
        self.screen = screen

    def update(self, events: list[pygame.event]) -> bool:
        shouldContinue = True
        for event in events:
            if event.type == pygame.QUIT:
                shouldContinue = False
        return shouldContinue
        
