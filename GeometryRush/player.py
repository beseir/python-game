import pygame
import math
from entity import Entity

class Player(Entity):
    
    def __init__(self, start_position=None, speed=4, rotation_speed=4):
        self.original_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, (0, 128, 255), [(50, 25), (0, 0), (0, 50)])
        
        super().__init__(self.original_image, start_position or pygame.math.Vector2(500, 200))
        
       
        self.speed = speed
        self.angle = 0
        self.rotation_speed = rotation_speed
        
     
        self._coins = 0

        self.velocity = pygame.Vector2(0, 0)

    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, value):
        if value < 0:
            raise ValueError("монетки не могут быть меньше нуля")
        self._coins = value


    def movement_input(self):
        keys = pygame.key.get_pressed()
        movement = pygame.math.Vector2(0, 0)
        
        if keys[pygame.K_LEFT]:
            movement.x -= 1
        if keys[pygame.K_RIGHT]:
            movement.x += 1
        if keys[pygame.K_UP]:
            movement.y -= 1
        if keys[pygame.K_DOWN]:
            movement.y += 1
            
        return movement
    
    def update_position(self, movement):
        if movement.length() > 0:
            normalized_movement = movement.normalize() * self.speed
            self.position += normalized_movement
            self.rect.center = self.position
        
        if self.velocity.length() > 0:
            self.position += self.velocity
            self.velocity *= 0.6
            self.rect.center = self.position
        
        

    def update_rotation(self, movement):
        if movement.length() > 0:
            target_angle = math.degrees(math.atan2(-movement.y, movement.x))
            angle_diff = (target_angle - self.angle + 180) % 360 - 180
            
            if angle_diff > self.rotation_speed:
                self.angle += self.rotation_speed
            elif angle_diff < -self.rotation_speed:
                self.angle -= self.rotation_speed
            else:
                self.angle = target_angle
            
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
       
        movement = self.movement_input()
        
        self.update_rotation(movement)
        self.update_position(movement)
        
        self.rect.center = self.position