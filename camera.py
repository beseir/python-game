import pygame
import math
import random
import sys

class Camera:
    def __init__(self, pos, screen_size, angle=0, zoom=1):
        self.pos = pygame.Vector2(pos)
        self.angle = angle
        self.zoom = zoom
        self.screen_center = pygame.Vector2(screen_size[0] // 2, screen_size[1] // 2)

        self.shake_end_time = 0
        self.shake_magnitude = 5
        self.shake_duration = 0

    def apply(self, pos):

        p = pygame.Vector2(pos) - self.pos
        p *= self.zoom
        rad = math.radians(self.angle)

        rotated_x = p.x * math.cos(rad) - p.y * math.sin(rad)
        rotated_y = p.x * math.sin(rad) + p.y * math.cos(rad)

        current_time = pygame.time.get_ticks()
        if current_time < self.shake_end_time:
            time_left = self.shake_end_time - current_time
            
            fraction = time_left / self.shake_duration

            amplitude = self.shake_magnitude * fraction

            rotated_x += random.uniform(-amplitude, amplitude)
            rotated_y += random.uniform(-amplitude, amplitude)

        return pygame.Vector2(rotated_x, rotated_y) + self.screen_center

    def shake(self, shake_duration: float, shake_magnitude: float = 5):
        """
            shake_duration - время тряски в секундах
            shake_magnitude - амплитуда тряски
        """
        current_time = pygame.time.get_ticks()
        self.shake_duration = int(shake_duration * 1000)
        self.shake_end_time = current_time + self.shake_duration

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
            sprite.draw(surface, self)