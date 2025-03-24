import pygame
from globals import globals
import random

class Entity(pygame.sprite.Sprite):
    def __init__(self, image=None, start_position=None ):
        super().__init__()
        self.image = image if image else pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(start_position) if start_position else pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        self.direction = pygame.math.Vector2(0, 0)
        self.max_health = 100
        self.health = 100
        self.show_health = False
        self.game = globals["game"]

        self.bar_ratio = None
        self.bar_bg_color = None
        self.bar_fg_color = None

    def damage(self, damage: int, attacker_position: pygame.Vector2 = None):
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

            health_ratio = self.health / self.max_health
            current_bar_width = int(bar_width * health_ratio)

            pygame.draw.rect(surface, (100, 100, 100), camera.apply_rect(pygame.Rect(bar_x, bar_y, bar_width, bar_height)))
            pygame.draw.rect(surface, (255, 0, 255), camera.apply_rect(pygame.Rect(bar_x, bar_y, current_bar_width, bar_height)))

        # custom bar
        if self.bar_ratio is not None:
            bar_width = 50
            bar_height = 6
            bar_x = self.rect.x + (self.rect.width - bar_width) / 2
            bar_y = self.rect.top - (bar_height - 4) * 10

            current_bar_width = int(bar_width * self.bar_ratio)

            pygame.draw.rect(surface, self.bar_bg_color, camera.apply_rect(pygame.Rect(bar_x, bar_y, bar_width, bar_height)))
            pygame.draw.rect(surface, self.bar_fg_color, camera.apply_rect(pygame.Rect(bar_x, bar_y, current_bar_width, bar_height)))
    
    def set_bar(self, ratio, bg_color, fg_color):
        self.bar_ratio = ratio
        self.bar_bg_color = bg_color
        self.bar_fg_color = fg_color

    def drop_coins(self, count):
        from GeometryRush.coin import Coin
        for _ in range(count):
            coin = Coin(self.position.x, self.position.y)
            coin.velocity = (self.velocity + self.direction * 1.5 + pygame.Vector2(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)).normalize() * 5) * random.uniform(0.0, max(count / 10.0, 10.0))
            self.game.add_coin(coin)