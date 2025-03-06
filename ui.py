import pygame 

class UI:
    def __init__(self, screen):
        self._elements = []
        self.screen = screen


    def add(self, element):
        self._elements.append(element)

    def update(self):
        [self.screen.blit(e.surface, e.position) for e in self._elements]