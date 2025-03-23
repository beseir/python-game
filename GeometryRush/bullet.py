import pygame
import math
from entity import Entity

class Bullet(Entity):
    
    def __init__(self, position, direction, power, producer, speed=20):
        self.original_image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, (13, 2, 1), [(0, 5), (30, 5), (30, 25), (0, 25)])

        super().__init__(self.original_image, position)
        
        self.power = power
        self.speed = speed
        self.angle = math.degrees(math.atan2(-direction.y, direction.x))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        self.direction = direction
        self.velocity = direction * speed

        self.update_position()



    
    def update_position(self):

        if self.velocity.length() > 0:
            self.position += self.velocity
            self.rect.center = self.position
        


    def update(self):
        self.update_position()