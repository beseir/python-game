from globals import globals
import socket

class YokeManager:
    def __init__(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = 11111
        self.udp_socket.setblocking(False)
        self.udp_socket.bind(("0.0.0.0", self.port))
        globals["yoke"] = self
        self.inputs = {}

        print(f"Ожидаем UDP-пакеты на порту {self.port}...\n")

    def update(self):
        while True:
            try:
                data, addr = self.udp_socket.recvfrom(1024)
                message = data.decode('utf-8').strip()

                parts = message.split()
                if len(parts) >= 7:
                    floats = list([float(part) for part in parts[:7]])

                    if addr[0] not in self.inputs:
                        print(f"новое udp подключение: {self.port}\n")
                        self.inputs[addr[0]] = YokeInput(addr[0])

                    self.inputs[addr[0]].update(floats)

                else:
                    print(f"⚠️ От {addr[0]} пришло меньше 7 значений: {parts}")

            except ValueError as ve:
                print(f"ошибка преобразования в float от {addr[0]}: {ve}")
            except BlockingIOError:
                # Данных нет, выходим из update
                return
            except Exception as e:
                print(f"yoke error: {e}")


import pygame
from input import Input
class YokeInput(Input):
    def __init__(self, ip):
        super().__init__()
        self.ip = ip
        self.view_direction = pygame.Vector2(1, 0)
    
    def update(self, floats):
        # floats[0..2] - акселерометр
        # floats[3..4] - x1, y1
        # floats[5..6] - x2, y2
        self.movement_direction = pygame.math.Vector2(floats[5], floats[6])
        if self.movement_direction.length() > 0:
            self.movement_direction = self.movement_direction.normalize()
        
        new_view_direction = pygame.math.Vector2(floats[3], floats[4])
        if new_view_direction.length() > 0:
            self.view_direction = pygame.math.Vector2(floats[3], floats[4]).normalize()
        elif self.movement_direction.length() > 0:
            self.view_direction = self.movement_direction
    
        self.attack = new_view_direction.length() > 0