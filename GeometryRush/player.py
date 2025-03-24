import random
import pygame
import math
from entity import Entity
from input import Input
from .bullet import Bullet

class Player(Entity):
    
    def __init__(self, input_controller: Input, start_position=None, speed=4, rotation_speed=4):
        self.original_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), [(50, 25), (0, 0), (0, 50)])
        
        super().__init__(self.original_image, start_position or pygame.math.Vector2(0, 0))
        
        self.input_controller = input_controller
        self.speed = speed
        self.angle = 0
        self.rotation_speed = rotation_speed
        self.cooldown_time = 100
        self.last_shoot_time = 0
        self.attack_pressed = False
     
        self.coins = 0
        self.show_health = True

        self.velocity = pygame.Vector2(0, 0)

    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, value):
        if value < 0:
            raise ValueError("монетки не могут быть меньше нуля")
        self._coins = value

    
    def update_position(self, movement):
        if movement.length() > 0:
            normalized_movement = movement.normalize() * self.speed
            self.position += normalized_movement
            self.rect.center = self.position
        
        if self.velocity.length() > 0:
            self.position += self.velocity
            self.velocity *= 0.9
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

        self.update_rotation(self.input_controller.view_direction)
        self.update_position(self.input_controller.movement_direction)

        self.set_bar(min(float(pygame.time.get_ticks() - self.last_shoot_time) / float(self.cooldown_time), 1.0), (255, 255, 255), (0, 0, 0))
        
        if not self.input_controller.attack and self.attack_pressed and pygame.time.get_ticks() - self.last_shoot_time >= self.cooldown_time:
            self.last_shoot_time = pygame.time.get_ticks()
            power = min(self.coins, 10)
            self.coins -= power
            power = max(1, power)
            self.game.add_bullet(Bullet(self.position, self.input_controller.view_direction, power, self))
        
        self.attack_pressed = self.input_controller.attack
            
        
        if (self.health <= 0):
            self.drop_coins(self.coins)
            self.kill()

        self.rect.center = self.position