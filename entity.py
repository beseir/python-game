import pygame
from globals import globals

class Entity(pygame.sprite.Sprite):
    def __init__(self, image=None, start_position=None ):
        super().__init__()
        self.image = image if image else pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(start_position) if start_position else pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        self.initial_health = 100
        self.health = 100
        self.show_health = False

    def damage(self, damage: float, attacker_position: pygame.Vector2 = None):
        if attacker_position != None:
            attack_direction = (self.position - attacker_position)
            if attack_direction.length() > 0:
                self.velocity += attack_direction.normalize() * 10
                self.health -= damage
                if "camera" in globals:
                    globals["camera"].shake(0.3, 5)
                
    def push(self, direction):
        self.velocity += direction.normalize() * 10

    def update(self):
        pass

    def draw(self, surface, camera):

        surface.blit(self.image, camera.apply_rect(self.rect))

        # health bar
        if self.show_health:
            bar_width = 50
            bar_height = 6
            bar_x = self.rect.x + (self.rect.width - bar_width) / 2
            bar_y = self.rect.top - bar_height - 4

            health_ratio = self.health / self.initial_health
            current_bar_width = int(bar_width * health_ratio)

            pygame.draw.rect(surface, (100, 100, 100), camera.apply_rect(pygame.Rect(bar_x, bar_y, bar_width, bar_height)))
            pygame.draw.rect(surface, (255, 0, 255), camera.apply_rect(pygame.Rect(bar_x, bar_y, current_bar_width, bar_height)))