import pygame

from entity import Entity
from .player import Player

class Coin(Entity):
    def __init__(self, x, y):
    
        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 242, 59))
        super().__init__(image=self.image, start_position=(x,y))
        self.rect = self.image.get_rect(center=self.position)
        
   

    def pickup(self, pickuper: Player):
        pickuper.coins += 1
        self.kill()