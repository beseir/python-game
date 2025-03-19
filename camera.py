import pygame
import math
import sys

class Camera:
    def __init__(self, pos, screen_size, angle=0, zoom=1):
        self.pos = pygame.Vector2(pos)
        self.angle = angle
        self.zoom = zoom
        self.screen_center = pygame.Vector2(screen_size[0] // 2, screen_size[1] // 2)

    def apply(self, pos):

        p = pygame.Vector2(pos) - self.pos
        p *= self.zoom
        rad = math.radians(self.angle)

        rotated_x = p.x * math.cos(rad) - p.y * math.sin(rad)
        rotated_y = p.x * math.sin(rad) + p.y * math.cos(rad)
        
        return pygame.Vector2(rotated_x, rotated_y) + self.screen_center


    def apply_rect(self, rect):

        center = self.apply(rect.center)
        
        w = rect.width * self.zoom
        h = rect.height * self.zoom
        
        return pygame.Rect(center.x - w / 2, center.y - h / 2, w, h)

    def draw_group(self, group, surface):
        """
        Перебирает все спрайты и отрисовывает их с применёнными преобразованиями камеры.
        """
        for sprite in group:
            transformed_rect = self.apply_rect(sprite.rect)
            surface.blit(sprite.image, transformed_rect)