import random
import pygame
from .coin import Coin
from .enemy import Enemy
from .firewall import Firewall
from .player import Player
from game import Game
from .GeometryRushUI import GeometryRushUI
from globals import globals
import input

class GameGeometryRush(Game):

    def __init__(self, screen, players: list[Player] = None):
        super().__init__(screen)

        globals["camera"] = self.camera

        self.BG_COLOR = (60, 255, 120)

        self.inputs = [
            input.InputKeyboard(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE),
            input.InputKeyboard(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL),
        ]
        self.players = list([Player(i) for i in self.inputs]) if players is None else players
        self.coins = pygame.sprite.Group()

        self.testEnemy = Enemy(self)
        self.firewall = Firewall(self)

        self.add(self.testEnemy)
        self.add(self.firewall)
        self.add(self.coins)
        self.add(self.players)

        self.coin_spawn_time = 1000 / len(self.players)
        self.coin_last_spawn_time = pygame.time.get_ticks()

        self.ui = GeometryRushUI(self.screen, self.players)

        self.direction = pygame.Vector2(1, 0)
        self.position = pygame.Vector2(0, 0)

    name = "Geometry Rush"

    def update(self, events: list[pygame.event]) -> bool:
        
        
        
        #чек колизий
        for player in self.players:
            collected_coins = pygame.sprite.spritecollide(player, self.coins, False)
            for coin in collected_coins:
                coin.pickup(player)

            if (pygame.sprite.collide_rect(player, self.firewall)):
                player.damage(1, player.position - self.direction)

            if (pygame.sprite.collide_rect(player, self.testEnemy)):
                player.damage(1, self.testEnemy.position)
            
            
        current_time = pygame.time.get_ticks()
        if current_time - self.coin_last_spawn_time > self.coin_spawn_time:
            new_coin = Coin(random.randint(int(self.camera.pos.x+1000), int(self.camera.pos.x+2000)), random.randint(int(self.camera.pos.y-200), int(self.camera.pos.y+200)))
            self.coins.add(new_coin)
            self.add(new_coin)
            self.coin_last_spawn_time = current_time 


        self.screen.fill(self.BG_COLOR)

        self.position += self.direction
        self.position.y += (sum(player.position.y for player in self.players) / len(self.players) - self.position.y) * 0.001
        camera_direction = (self.position - self.camera.pos)
        if camera_direction.length() > 0:
            self.camera.pos += camera_direction * 0.3
        
        [i.update() for i in self.inputs]
        shouldContinue = super().update(events)

        return shouldContinue


    def get_nearest_player(self, position):
        nearest_player = None
        min_distance = float('inf')

        for player in self.players:
            distance = position.distance_to(player.position)

            if distance < min_distance:
                min_distance = distance
                nearest_player = player

        return nearest_player