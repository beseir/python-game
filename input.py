import pygame


class Input:
    def __init__(self):
        self.movement_direction = pygame.Vector2(0, 0)
        self.view_direction = pygame.Vector2(1, 0)
        self.attack = False


class InputKeyboard(Input):
    def __init__(self, key_up, key_down, key_left, key_right, key_attack):
        super().__init__()
        self.key_up = key_up
        self.key_down = key_down
        self.key_left = key_left
        self.key_right = key_right
        self.key_attack = key_attack
    
    def update(self):
        keys = pygame.key.get_pressed()
        self.movement_direction = pygame.math.Vector2(0, 0)
        
        if keys[self.key_up]:
            self.movement_direction.y -= 1
        if keys[self.key_down]:
            self.movement_direction.y += 1
        if keys[self.key_left]:
            self.movement_direction.x -= 1
        if keys[self.key_right]:
            self.movement_direction.x += 1
            
        if self.movement_direction.length() > 0:
            self.view_direction = self.movement_direction
    
        self.attack = keys[self.key_attack]
