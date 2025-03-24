import pygame
from scene import Scene
from game import Game
from text import drawText
from globals import globals

globals["games"] = Game.__subclasses__()

class Menu(Scene):
    def __init__(self, screen):
        self.screen = screen
        self._entities = pygame.sprite.Group()

       
    @property
    def name(self):
        return "menu"

    def update(self, events: list[pygame.event]) -> bool:
        shouldContinue = super().update(events)

        mousePos = None

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = event.pos

        globals["screen"].fill((0, 0, 0))
        drawText(globals["screen"], "connected yoke devices: " + str(len(globals["yoke"].inputs.items())), 50, (255, 255, 255), (globals["screen"].get_size()[0]/2, 150/3), 0)

        i = 0
        for game in globals["games"]:
            i += 150
            center = (globals["screen"].get_size()[0]/2, i)
            width = 600
            height = 100
            rect = pygame.Rect(center[0]-width/2, center[1]-height/2, width, height)

            if mousePos != None:
                if rect.collidepoint(mousePos):
                    changeGame(game)

            pygame.draw.rect(globals["screen"], (200, 100, 10), rect=rect)

            drawText(globals["screen"], game.name, 70, (0, 0, 0), center, 0)
        # код рисования прямоугольников с текстом и кликами на них

        return shouldContinue
        


globals["selectedGame"] = Menu(globals["screen"])

def changeGame(TT):
    globals["selectedGame"] = TT(globals["screen"])
    pygame.display.set_caption(TT.name)


# game = GameGeometryRush(screen)
#     pygame.display.set_caption(game.name)