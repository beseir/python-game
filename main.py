import pygame
from GeometryRush.GeometryRush import GameGeometryRush

pygame.init()
screen = pygame.display.set_mode((888, 555))

def main():
    clock = pygame.time.Clock()
    running = True

    game = GameGeometryRush(screen)
    pygame.display.set_caption(game.name)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.update()
        pygame.display.flip()
        clock.tick(120)

    pygame.quit()

if __name__ == "__main__":
    main()
