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
        self.local_players = 0
        self.local_players_forced_set = False

        from input import InputKeyboard
        self.local_inputs = [
            InputKeyboard(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE),
            InputKeyboard(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL),
        ]

       
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

        center = (globals["screen"].get_size()[0]/2, 150/2)
        width = 400
        height = 50
        rect = pygame.Rect(center[0]-width/2, center[1]-height/2, width, height)
        pygame.draw.rect(globals["screen"], (10, 200, 200), rect=rect)
        drawText(globals["screen"], "local players: " + str(self.local_players), 70, (0, 0, 0), center, 0)
        if mousePos is not None and rect.collidepoint(mousePos):
            self.local_players = (self.local_players + 1) % (len(self.local_inputs) + 1)
            self.local_players_forced_set = True


        drawText(globals["screen"], "connected yoke devices: " + str(len(globals["yoke"].inputs.items())), 50, (255, 255, 255), (globals["screen"].get_size()[0]/2, 150), 0)

        i = 150
        for game in globals["games"]:
            i += 150
            center = (globals["screen"].get_size()[0]/2, i)
            width = 600
            height = 100
            rect = pygame.Rect(center[0]-width/2, center[1]-height/2, width, height)

            if mousePos != None:
                if rect.collidepoint(mousePos):
                    changeGame(game, self.generate_inputs())

            pygame.draw.rect(globals["screen"], (200, 100, 10), rect=rect)

            drawText(globals["screen"], game.name, 70, (0, 0, 0), center, 0)
        # код рисования прямоугольников с текстом и кликами на них

        return shouldContinue
    

    def generate_inputs(self):
        inputs = []

        local_players = self.local_players
        if local_players == 0 and len(globals["yoke"].inputs) == 0 and not self.local_players_forced_set:
            local_players = 1

        for i in range(local_players):
            inputs.append(self.local_inputs[i])

        for yoke_ip in globals["yoke"].inputs:
            inputs.append(globals["yoke"].inputs[yoke_ip])

        return inputs
        


globals["selectedGame"] = Menu(globals["screen"])

def changeGame(TT, inputs):
    globals["selectedGame"] = TT(globals["screen"], inputs)
    pygame.display.set_caption(TT.name)


# game = GameGeometryRush(screen)
#     pygame.display.set_caption(game.name)