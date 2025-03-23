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
from .bullet import Bullet

class GameGeometryRush(Game):

    def __init__(self, screen, players: list[Player] = None):
        super().__init__(screen)

        globals["camera"] = self.camera

        self.BG_COLOR = (60, 255, 120)

        self.bullets = pygame.sprite.Group()
        self.inputs = [
            input.InputKeyboard(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE),
            # input.InputKeyboard(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL),
        ]
        self.players = pygame.sprite.Group(list([Player(i) for i in self.inputs])) if players is None else players
        self.coins = pygame.sprite.Group()

        self.enemies = pygame.sprite.Group()
        self.defeated_enemies = 0
        self.enemies_to_win = 150
        self.firewall = Firewall(self)

        self.add(self.enemies)
        self.add(self.firewall)
        self.add(self.coins)
        self.add(self.players)

        self.coin_spawn_time = 1000 / max(len(self.players), 1)
        self.coin_last_spawn_time = pygame.time.get_ticks()

        self.ui = GeometryRushUI(self.screen, self.players)

        self.direction = pygame.Vector2(1, 0)
        self.position = pygame.Vector2(0, 0)

    name = "Geometry Rush"

    def add_bullet(self, bullet):
        self.bullets.add(bullet)
        self.add(bullet)

    def add_coin(self, coin):
        self.coins.add(coin)
        self.add(coin)

    def add_enemy(self, enemy):
        self.enemies.add(enemy)
        self.add(enemy)

    def update(self, events: list[pygame.event]) -> bool:
        
        
        
        #чек колизий
        for player in self.players:
            if pygame.key.get_pressed()[pygame.K_k]:
                player.health = 0
            if pygame.key.get_pressed()[pygame.K_c]:
                player.coins += 1

            collected_coins = pygame.sprite.spritecollide(player, self.coins, False)
            for coin in collected_coins:
                coin.pickup(player)

            if (pygame.sprite.collide_rect(player, self.firewall)):
                player.damage(1, player.position - self.direction)

            for enemy in self.enemies:
                if (pygame.sprite.collide_rect(player, enemy)):
                    player.damage(1, enemy.position)
        

        for bullet in self.bullets:
            if (pygame.sprite.collide_rect(bullet, self.firewall)):
                
                direction1 = (-bullet.direction + self.direction.rotate( 90) + self.direction * 0.01).normalize()
                direction2 = (-bullet.direction + self.direction.rotate(-90) + self.direction * 0.01).normalize()

                bullet1 = Bullet(bullet.position + direction1 * 10, direction1, int(bullet.power/2), None)
                bullet2 = Bullet(bullet.position + direction2 * 10, direction2, int(bullet.power/2), None)

                if int(bullet.power/2) == 0:
                    bullet1.drop_coins(1)
                    bullet2.drop_coins(1)
                else:
                    self.add_bullet(bullet1)
                    self.add_bullet(bullet2)
                
                if bullet.power % 2 == 1:
                    bullet.drop_coins(1)
                
                bullet.kill()
            
            for enemy in self.enemies:
                if pygame.sprite.collide_rect(bullet, enemy):
                    enemy.damage(bullet.power, bullet.position)
                    bullet.kill()
            
        for coin in self.coins:
            if pygame.sprite.collide_rect(coin, self.firewall):
                coin.push(self.direction)


        for enemy1 in self.enemies:
            for enemy2 in self.enemies:
                if (enemy1 == enemy2):
                    continue
                
                if pygame.sprite.collide_rect(enemy1, enemy2):
                    enemy1.push(enemy1.position - enemy2.position)
        
            
        current_time = pygame.time.get_ticks()
        if current_time - self.coin_last_spawn_time > self.coin_spawn_time:
            new_coin = Coin(random.randint(int(self.camera.pos.x+1000), int(self.camera.pos.x+2000)), random.randint(int(self.camera.pos.y-200), int(self.camera.pos.y+200)))
            self.coins.add(new_coin)
            self.add(new_coin)
            self.coin_last_spawn_time = current_time 

        if len(self.enemies) < len(self.players):
            # в начале игры, когда убито мало врагов, будут спавнится в основном лёгкие (значение r будет близко к 1.0)
            # а под конец игры значение r в среднем будет уменьшаться
            r = random.random() ** (self.defeated_enemies / (self.enemies_to_win*0.6))
            # ЧЕМ МЕНЬШЕ r - ТЕМ СЛОЖНЕЕ ДОЛЖЕН БЫТЬ ПРОТИВНИК

            position = pygame.Vector2(random.uniform(self.camera.pos.x+1000, self.camera.pos.x+4000), random.uniform(self.camera.pos.y-300, self.camera.pos.y+300))
            if r < 0.1:
                print("hard enemy!")
                enemy = Enemy(position, self)
                print("enemy added:", enemy.position)
            else:
                enemy = Enemy(position, self)
                print("enemy added:", enemy.position)

            self.add_enemy(enemy)


        self.screen.fill(self.BG_COLOR)

        self.position += self.direction
        self.position.y += (sum(player.position.y for player in self.players) / max(len(self.players), 1) - self.position.y) * 0.001
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