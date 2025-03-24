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

        self.attack_types = []
        self.attack_types.append(AttackTypeBullet())
        self.attack_types.append(AttackTypeHardBullet())
        self.last_shoot_time = pygame.time.get_ticks()
        self.attack_type_index = 0
        self.attack_pressed = False
        self.attack_pressed_time = None
        self.attack_changeing_time = None
        self.attack_bar_background = (0, 0, 0)
     
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

    def attack_update(self):

        if self.attack_pressed_time is None:
            ratio = float(pygame.time.get_ticks() - self.last_shoot_time) / float(self.cooldown_time)

            self.set_bar(float(min(ratio, 1.0)), self.attack_bar_background, (255, 255, 255))
            if ratio > 1.0:
                self.attack_bar_background = (255, 255, 255)
        else:
            if (pygame.time.get_ticks() - self.attack_changeing_time > self.attack_types[self.attack_type_index].time_to_load * 1000) and len(self.attack_types) > self.attack_type_index + 1:
                self.attack_changeing_time += self.attack_types[self.attack_type_index].time_to_load * 1000
                self.attack_bar_background = self.attack_types[self.attack_type_index].color
                self.attack_type_index += 1
            
            ratio = float(pygame.time.get_ticks() - self.attack_changeing_time) / float(self.attack_types[self.attack_type_index].time_to_load * 1000)
            self.set_bar(min(ratio, 1.0), self.attack_bar_background, self.attack_types[self.attack_type_index].color)

        
        if not self.input_controller.attack and self.attack_pressed and pygame.time.get_ticks() - self.last_shoot_time >= self.cooldown_time:
            # кнопка атаки отпустилась
            self.attack_pressed_time = None
            self.attack_changeing_time = None

            self.last_shoot_time = pygame.time.get_ticks()
            attack_type_index = self.attack_type_index
            if ratio < 0.5 and attack_type_index > 0:
                attack_type_index -= 1
                
            self.attack_types[attack_type_index].attack(self, self.game)
            self.attack_bar_background = self.attack_types[attack_type_index].color
            self.attack_type_index = 0

            

        if self.input_controller.attack and not self.attack_pressed:
            # кнопка атаки нажалась
            self.attack_pressed_time = pygame.time.get_ticks()
            self.attack_changeing_time = pygame.time.get_ticks()
        
        self.attack_pressed = self.input_controller.attack
            

    def update(self):

        self.update_rotation(self.input_controller.view_direction)
        self.update_position(self.input_controller.movement_direction)
        self.attack_update()

        if (self.health <= 0):
            self.drop_coins(self.coins)
            self.kill()

        self.rect.center = self.position


class AttackType:
    def __init__(self):
        self.time_to_load = 0.0
        self.color = (0, 0, 0)
    
    def attack(self, entity, game, ):
        pass

class AttackTypeBullet:
    def __init__(self):
        self.time_to_load = 1.0
        self.color = (0, 0, 0)

    def attack(self, entity, game):
        if hasattr(entity, "coins"):
            power = min(entity.coins, 5)
            entity.coins -= power
            power = max(1, power)
        else:
            power = 1
        game.add_bullet(Bullet(entity.position, entity.input_controller.view_direction, power, entity))

class AttackTypeHardBullet:
    def __init__(self):
        self.time_to_load = 2.0
        self.color = (200, 0, 0)

    def attack(self, entity, game):
        if hasattr(entity, "coins"):
            power = min(entity.coins, 20)
            entity.coins -= power
            power = max(5, power)
        else:
            power = 5
        game.add_bullet(Bullet(entity.position, entity.input_controller.view_direction, power, entity))