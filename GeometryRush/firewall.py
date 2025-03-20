import pygame

from entity import Entity

class Firewall(Entity):
    def __init__(self, game):
        self.image = pygame.Surface((50, 10000))
        self.image.fill((255, 0, 0))
      
        super().__init__(self.image, pygame.math.Vector2(0, 0))

        self.game = game


    def update(self):
        self.rect = self.image.get_rect(center=self.position)
        self.position = (self.game.position.x - self.game.screen.get_size()[0] / 2, self.game.position.y - self.image.get_size()[1]/4)
