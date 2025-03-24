import pygame
from text import drawText
from globals import globals 
from GeometryRush import GeometryRush

pygame.init()
# globals["screen"] = pygame.display.set_mode((888, 555), pygame.RESIZABLE | pygame.FULLSCREEN)
globals["screen"] = pygame.display.set_mode((888, 555), pygame.RESIZABLE)

from yoke import YokeManager
yoke = YokeManager()

import menu
# импорт меню после инициализации pygame, потому что
# в menu.py используется screen

def main():
    clock = pygame.time.Clock()
    running = True

    while running:

        yoke.update()
        running = globals["selectedGame"].update(pygame.event.get())
        pygame.display.flip()
        clock.tick(120)

    pygame.quit()

if __name__ == "__main__":
    main()
