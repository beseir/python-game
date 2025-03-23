import pygame

from entity import Entity

class Firewall(Entity):
    def __init__(self, game):
        self.image = pygame.Surface(game.screen.get_size())
        super().__init__(self.image, pygame.math.Vector2(0, 0))

        self.image.set_alpha(0)


    def update(self):
        self.rect = self.image.get_rect(center=self.position)
        self.position = pygame.Vector2(self.game.position.x, self.game.position.y)

    def direction_to_center(self, position):
        # move_x = 0
        # move_y = 0

        # if position.x < self.position.x:
        #     move_x = self.position.x - position.x
        # elif position.x > self.position.x:
        #     move_x = self.position.x - position.x

        # if position.y < self.position.y:
        #     move_y = self.position.y - position.y
        # elif position.y > self.position.y:
        #     move_y = self.position.y - position.y

        
        # if abs(move_x) < abs(move_y):
        #     return pygame.Vector2(move_x, 0)
        # else:
        #     return pygame.Vector2(0, move_y)

        return (self.position - position).normalize()
