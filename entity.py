import pygame
from globals import globals

class Entity(pygame.sprite.Sprite):
    def __init__(self, image=None, start_position=None ):
        super().__init__()
        self.image = image if image else pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(start_position) if start_position else pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)

    def damage(self, damage: float, attacker_position: pygame.Vector2 = None):
        if attacker_position != None:
            attack_direction = (self.position - attacker_position)
            if attack_direction.length() > 0:
                self.velocity += attack_direction.normalize() * 10
                if "camera" in globals:
                    globals["camera"].shake(0.3, 5)

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)