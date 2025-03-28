# import constants_for_map
import math
import random

from src.back.constants_with_paths_to_files import PATH_TO_ENEMY
from src.back.player import *

kSizeOfCharacter = 48
kSize_of_enemy = 48
WINDOW_SIZE = [1920, 1000]
kSize_of_display = WINDOW_SIZE
kSpawnPosition = [kSize_of_display[0] // 2, kSize_of_display[1] // 2]


class Enemy:
    def __init__(self):
        self.speed = 1
        self.image = pygame.Surface((kSize_of_enemy, kSize_of_enemy), flags=pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.image_of_character = pygame.image.load(PATH_TO_ENEMY)
        self.image_of_character = pygame.transform.scale(self.image_of_character, (kSize_of_enemy, kSize_of_enemy))
        self.image.blit(self.image_of_character, (0, 0))
        self.x, self.y = 1920 / 2, 1000 / 2
        self.dead = False  # жив или не
        self.health = 3  # колво жизней
        self.hurt_distance = 72  # расстояние где проиивник модет стрелять
        self.velocity = [0, 0]
        self.rect = self.image.get_rect()
        self.enemies = []
        self.direction = [0, 0]
        self.moveBox = (
            kSize_of_display[0] // 2 - SIZE_OF_MOVE_BOX[0] // 2, kSize_of_display[1] // 2 - SIZE_OF_MOVE_BOX[1] //
            2, kSize_of_display[0] // 2 + SIZE_OF_MOVE_BOX[0] // 2,
            kSize_of_display[1] // 2 + SIZE_OF_MOVE_BOX[1] // 2)
        self.direction = [0, 0]

    def die(self):  # для удаления
        if not self.dead:
            self.dead = True

    def set_velocity(self, new_velocity):
        self.velocity = new_velocity

    def hurt(self, live):  # метод нанесения урона
        if not self.dead:
            self.health -= live
            if self.health <= 0:
                self.die()

    def move(self, mappa, player_pos):
        self.direction = [0, 0]
        dx, dy = player_pos[0] - self.x, player_pos[1] - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        velocity = None

        if distance != 0:
            # вычисляем вектор направления движения
            direction = [dx / distance, dy / distance]
            # ограничиваем скорость врага
            velocity = [direction[0] * self.speed, direction[1] * self.speed]

            if self.rect.centerx < self.moveBox[0]:
                self.direction[0] = self.speed
            elif self.rect.centerx > self.moveBox[2]:
                self.direction[0] = -self.speed
            else:
                self.direction[0] = random.choice([-self.speed, 0, self.speed])

            if self.rect.centery < self.moveBox[1]:
                self.direction[1] = self.speed
            elif self.rect.centery > self.moveBox[3]:
                self.direction[1] = -self.speed
            else:
                self.direction[1] = random.choice([-self.speed, 0, self.speed])

            if self.direction[0] < 0 and not mappa.CanStandThere(
                    (self.x + self.direction[0], self.y + kSizeOfCharacter)):
                self.direction[0] = 0

            elif self.direction[0] > 0 and not mappa.CanStandThere(
                    (self.x + kSizeOfCharacter + self.direction[0], self.y + kSizeOfCharacter)):
                self.direction[0] = 0
        self.x += velocity[0]
        self.y += velocity[1]

    def render(self, display):
        display.blit(self.image, (self.x, self.y))
