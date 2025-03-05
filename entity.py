import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, image=None, start_position=None ):
        super().__init__()
        self.image = image if image else pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(start_position) if start_position else pygame.math.Vector2(0, 0)

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)