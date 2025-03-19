import pygame

from entity import Entity
from .player import Player

class Enemy(Entity):
    def __init__(self, target: Player):
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 22, 22))
      
        super().__init__(self.image, pygame.math.Vector2(0, 0))

        self.target = target
        self.speed = 1.5


    def update(self):
        movement = (self.target.position - self.position)
        if (movement.length() > 1):
            movement = movement.normalize()

        self.rect = self.image.get_rect(center=self.position)

        self.position = self.position + movement * self.speed
