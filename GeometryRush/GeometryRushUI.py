import pygame
from ui import UI
from ui_element import UIElement
class GeometryRushUI(UI):
    def __init__(self, screen, player):
        super().__init__(screen)
        self.player = player
        self.font = pygame.font.Font(None, 35)
        self.coins_text = self.font.render(str(self.player.coins), True, (0, 0, 0))
        self.coins_text_rect = self.coins_text.get_rect(center=(50, 30)) 
        self.coins_element = UIElement(self.coins_text, self.coins_text_rect)

        self.add(self.coins_element)

    def update(self):
        self.coins_element.surface =  self.font.render(str(self.player.coins), True, (0, 0, 0))
        super().update()