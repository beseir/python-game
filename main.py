import pygame
from text import drawText
from globals import globals 
from GeometryRush import GeometryRush

pygame.init()
globals["screen"] = pygame.display.set_mode((888, 555), pygame.RESIZABLE)

import menu
# импорт меню после инициализации pygame, потому что
# в menu.py используется screen


def main():
    clock = pygame.time.Clock()
    running = True

    while running:

        running = globals["selectedGame"].update(pygame.event.get())
        pygame.display.flip()
        clock.tick(120)

    pygame.quit()

if __name__ == "__main__":
    main()
