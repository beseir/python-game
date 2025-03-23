import pygame

from entity import Entity
from .player import Player

class Enemy(Entity):
    def __init__(self, position, game):
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 22, 22))
      
        super().__init__(self.image, pygame.math.Vector2(0, 0))

        self.position = position

        self.game = game
        self.speed = 1.5
        self.max_health = 20 * self.game.difficulty
        self.health = self.max_health
        self.show_health = True


    def update(self):
        self.target = self.game.get_nearest_player(self.position)
        if self.target is None:
            return
            
        movement = (self.target.position - self.position)
        if (movement.length() > 1):
            movement = movement.normalize()

        self.rect = self.image.get_rect(center=self.position)

        self.position = self.position + movement * self.speed
        self.position += self.velocity * 0.4
        self.velocity *= 0.9

        if self.health <= self.max_health * 0.05:
            self.drop_coins(int(25 * self.game.difficulty))
            self.kill()
            self.game.defeated_enemies += 1
