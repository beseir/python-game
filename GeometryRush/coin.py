import pygame

from entity import Entity

class Coin(Entity):
    def __init__(self, x, y):
    
        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 242, 59))
        super().__init__(image=self.image, start_position=(x,y))
        self.rect = self.image.get_rect(center=self.position)
        
   

    def pickup(self, pickuper):
        pickuper.coins += 1
        self.kill()
    
    def update(self):
        if self.velocity.length() > 0:
            self.position += self.velocity
            self.velocity *= 0.9
            self.rect.center = self.position