import pygame

from entity import Entity
from .player import Player

class EnemyChain(Entity):
    def __init__(self, position, game):
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (139, 69, 19), (25, 25), 25, 0)
      
        super().__init__(self.image, pygame.math.Vector2(0, 0))

        self.position = position

        self.game = game
        self.speed = 1.5
        self.max_health = 40 * self.game.difficulty
        self.health = self.max_health
        self.show_health = True


    def update(self):

        self.acceleration = pygame.Vector2(0, 0)
        for player in self.game.players:
            direction = player.position - self.position
            if direction.length() > 300:
                self.acceleration += direction
        if self.acceleration.length() > 1:
            self.acceleration = self.acceleration.normalize() * (self.acceleration.length() / 300)
            
        self.velocity += self.acceleration
        self.velocity += self.game.firewall.direction_to_center(self.position) * 0.01
        if self.velocity.length() > 10:
            self.velocity = self.velocity.normalize() * 10
        self.rect = self.image.get_rect(center=self.position)

        self.position += self.velocity * 0.9

        if self.health <= self.max_health * 0.05:
            self.drop_coins(int(100 * self.game.difficulty))
            self.kill()
            self.game.defeated_enemies += 1
