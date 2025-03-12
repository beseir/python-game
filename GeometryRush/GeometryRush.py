import random
import pygame
from .coin import Coin
from .enemy import Enemy
from .player import Player
from game import Game
from .GeometryRushUI import GeometryRushUI


class GameGeometryRush(Game):

    def __init__(self, screen):
        super().__init__(screen)

        self.BG_COLOR = (60, 255, 120)
        self.entities = pygame.sprite.Group()

        self.player = Player()
        self.coins =  self.spawn_coins()

        self.testEnemy = Enemy(self.player)

        self.add(self.testEnemy)
        self.add(self.coins)
        self.add(self.player)

        self.coin_spawn_time = 2000
        self.coin_last_spawn_time = pygame.time.get_ticks()

        self.ui = GeometryRushUI(self.screen, self.player)


    
    def spawn_coins(self):
        coins = pygame.sprite.Group()
        for _ in range(5):
            coin = Coin(random.randint(50, 750), random.randint(50, 550))
            coins.add(coin)
        return coins

    name = "Geometry Rush"

    def update(self, events: list[pygame.event]) -> bool:
        shouldContinue = super().update(events)
        
        [e.update() for e in self._entities]
        
        #чек колизий
        collected_coins = pygame.sprite.spritecollide(self.player, self.coins, False)
        for coin in collected_coins:
            coin.pickup(self.player)  
            
        current_time = pygame.time.get_ticks()
        if current_time - self.coin_last_spawn_time > self.coin_spawn_time:
            new_coin = Coin(random.randint(50, 750), random.randint(50, 550))
            self.coins.add(new_coin)
            self.add(new_coin)
            self.coin_last_spawn_time = current_time 


        self.screen.fill(self.BG_COLOR)
        self._entities.draw(self.screen)

        return shouldContinue
