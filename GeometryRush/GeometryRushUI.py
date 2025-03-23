import pygame
from ui import UI
from ui_element import UIElement

class GeometryRushUI(UI):
    width_for_player = 100
    def __init__(self, screen, players):
        super().__init__(screen)
        self.players = players
        self.font = pygame.font.Font(None, 35)

        self.surface_width = self.width_for_player * len(self.players)
        self.surface_height = 40
        self.surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)

        self.rect = self.surface.get_rect(topleft=(0, 0))
        self.coins_element = UIElement(self.surface, self.rect)

        self.add(self.coins_element)

    def update(self):
        new_width = self.width_for_player * len(self.players)
        if new_width != self.surface.get_width():
            self.surface = pygame.Surface((new_width, self.surface_width), pygame.SRCALPHA)
            self.coins_element.surface = self.surface
            self.coins_element.rect = self.surface.get_rect(topleft=(0, 0))

        self.surface.fill((0, 0, 0, 0))

        for index, player in enumerate(self.players):
            text = self.font.render(f"{index + 1}: {player.coins}", True, (0, 0, 0))
            self.surface.blit(text, (index * self.width_for_player, 10))

        super().update()
