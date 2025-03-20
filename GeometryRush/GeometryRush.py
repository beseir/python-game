import random
import pygame
from .coin import Coin
from .enemy import Enemy
from .firewall import Firewall
from .player import Player
from game import Game
from .GeometryRushUI import GeometryRushUI


class GameGeometryRush(Game):

    def __init__(self, screen):
        super().__init__(screen)

        self.BG_COLOR = (60, 255, 120)

        self.player = Player()
        self.coins =  self.spawn_coins()

        self.testEnemy = Enemy(self.player)
        self.firewall = Firewall(self)

        self.add(self.testEnemy)
        self.add(self.firewall)
        self.add(self.coins)
        self.add(self.player)

        self.coin_spawn_time = 2000
        self.coin_last_spawn_time = pygame.time.get_ticks()

        self.ui = GeometryRushUI(self.screen, self.player)

        self.direction = pygame.Vector2(1, 0)
        self.position = pygame.Vector2(0, 0)


    
    def spawn_coins(self):
        coins = pygame.sprite.Group()
        for _ in range(5):
            coin = Coin(random.randint(50, 750), random.randint(50, 550))
            coins.add(coin)
        return coins

    name = "Geometry Rush"

    def update(self, events: list[pygame.event]) -> bool:
        
        
        
        #чек колизий
        collected_coins = pygame.sprite.spritecollide(self.player, self.coins, False)
        for coin in collected_coins:
            coin.pickup(self.player)

        if (pygame.sprite.collide_rect(self.player, self.firewall)):
            self.camera.shake(0.2)
            self.player.velocity = self.direction * 100

        if (pygame.sprite.collide_rect(self.player, self.testEnemy)):
            self.camera.shake(0.2)
            self.player.velocity = (self.player.position - self.testEnemy.position).normalize() * 100
            
        current_time = pygame.time.get_ticks()
        if current_time - self.coin_last_spawn_time > self.coin_spawn_time:
            new_coin = Coin(random.randint(int(self.camera.pos.x+1000), int(self.camera.pos.x+2000)), random.randint(int(self.camera.pos.y-200), int(self.camera.pos.y+200)))
            self.coins.add(new_coin)
            self.add(new_coin)
            self.coin_last_spawn_time = current_time 


        self.screen.fill(self.BG_COLOR)

        self.position += self.direction
        self.position += (self.player.position - self.position) * 0.001
        camera_direction = (self.position - self.camera.pos)
        if camera_direction.length() > 0:
            self.camera.pos += camera_direction * 0.3
        
        shouldContinue = super().update(events)

        return shouldContinue
