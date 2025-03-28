import math
from src.back.player import *
from src.back.constants_with_paths_to_files import PATH_TO_ENEMY
from src.back.projectile import *
import time
from src.back.Config import *
from abc import ABC, abstractmethod

kSizeOfCharacter = 48
kSizeOfEnemy = 48
kSizeOfProjectile = 32


class Enemy:
    def __init__(self, spawn_position, health, size=kSizeOfEnemy):
        self.speed = 2
        self.sleep_speed = 1
        self.health = health
        self.size = size
        self.direction = [0, 0]
        self.ImageOfCharacter = pygame.image.load(PATH_TO_ENEMY)
        self.ImageOfCharacter = pygame.transform.scale(self.ImageOfCharacter, (self.size, self.size))
        self.rect = self.ImageOfCharacter.get_rect(topleft=spawn_position)
        self.spawn_position = spawn_position
        self.health = health  # колво жизней
        self.num_of_frames_with_movement = 0

        # ниже все добавлено для атаки:enemies
        # self.max_magic = 1000
        # self.magic_points = self.max_magic
        # self.last_fire_time = 1
        # self.cool_down = 3  # скорострельность оружия
        # self.max_distance = 1000  # расстояние, где противник может стрелять
        # self.ranged_attack_damage = 20
        # self.fires = []
        # self.dist = 300  # Рандомное число
        # self.cur_dist = 0

    def IsAlive(self):  # для удаления
        return self.health > 0

    def Hurt(self, damage):  # метод нанесения урона
        self.health -= damage

    def ChasePlayer(self, mappa, player_position):
        enemy_position = self.rect.x, self.rect.y

        self.dx = player_position[0] - enemy_position[0]
        self.dy = player_position[1] - enemy_position[1]
        distance = math.sqrt(self.dx * self.dx + self.dy * self.dy)

        if distance <= 70:
            self.direction = [0, 0]
        else:
            if distance > 0:
                self.direction[0] = self.dx / distance
                self.direction[1] = self.dy / distance

            # проверка тапла:
            if self.direction != [0, 0]:
                self.direction = normalized(self.direction)
                self.direction[0] *= self.speed
                self.direction[1] *= self.speed

                self.direction[0] = round(self.direction[0])
                self.direction[1] = round(self.direction[1])

                if self.direction[0] < 0 and not mappa.CanStandThere(
                        (self.rect.x + self.direction[0], self.rect.y + kSizeOfEnemy)):
                    self.direction[0] = 0

                elif self.direction[0] > 0 and not mappa.CanStandThere(
                        (self.rect.x + kSizeOfEnemy + self.direction[0], self.rect.y + kSizeOfEnemy)):
                    self.direction[0] = 0

                if self.direction[1] < 0 and not mappa.CanStandThere(
                        (self.rect.x, self.rect.y + kSizeOfEnemy - 8 + self.direction[1])) or not mappa.CanStandThere(
                    (self.rect.x + kSizeOfEnemy, self.rect.y + kSizeOfEnemy - 8 + self.direction[1])):
                    self.direction[1] = 0

                elif self.direction[1] > 0 and not mappa.CanStandThere(
                        (self.rect.x, self.rect.y + kSizeOfEnemy + self.direction[1])) or not mappa.CanStandThere(
                    (self.rect.x + kSizeOfEnemy, self.rect.y + kSizeOfEnemy + self.direction[1])):
                    self.direction[1] = 0

                self.rect.x += self.direction[0]
                self.rect.y += self.direction[1]

                # def shoot_player(self, player_position, current_time):
                #     if current_time - self.last_shoot_time >= timedelta(
                #             seconds=1.5):  # проверяем прошло ли уже 1.5 секунды с прошлого выстрела
                #         distance = math.sqrt(
                #             (self.rect[0] - player_position[0]) ** 2 + (self.rect[1] - player_position[1]) ** 2)
                #
                #         if distance <= self.max_distance:
                #             direction = [player_position[0] - self.rect.x, player_position[1] - self.rect.y]
                #             fireball = Projectile(self.ranged_attack_damage, (self.rect.x, self.rect.y), player_position,
                #                                   distance, direction, 100, 0.5, magic_wizard)
                #             self.fires.append(fireball)
                #             self.magic_points -= 100
                #             self.last_shoot_time = current_time

                # def render(self, display, player_pos, player_pos_on_screen):
                #     display.blit(self.image,
                #                  (self.rect.x - player_pos[0] + player_pos_on_screen[0],
                #                   self.rect.y - player_pos[1] + player_pos_on_screen[1]))
                #     display.blit(self.image,
                #                  (self.rect.x - player_pos[0] + player_pos_on_screen[0],
                #                   self.rect.y - player_pos[1] + player_pos_on_screen[1]))
                #     if self.fires:
                #         for (i, fire) in enumerate(self.fires):
                #             if fire.render(display, player_pos_on_screen, player_pos):
                #                 self.fires.pop(i)

                # def update(self, mappa, player_position, current_time, player):
                #     self.ChasePlayer(mappa, player_position)
                #     # self.shoot_player(player_position, current_time)
                #     if self.fires:
                #         for (i, fire) in enumerate(self.fires):
                #             if fire.update(mappa):
                #                 self.fires.pop(i)
                #
                #     if self.rect.colliderect(player.rect):
                #         player.health_points -= self.ranged_attack_damage

                def SlowMove(self):
                    if self.num_of_frames_with_movement > 0:
                        self.rect.x += self.direction[0]
                        self.rect.y += self.direction[1]
                        self.num_of_frames_with_movement = max(self.num_of_frames_with_movement - 1, 0)

                def StopMovement(self):
                    self.num_of_frames_with_movement = 0

                def GetDirectionOfMovement(self):
                    return self.direction

                def IsMove(self):
                    return self.num_of_frames_with_movement > 0

                def SetDirectionOfMovement(self, direction, num_of_frames):
                    self.num_of_frames_with_movement = num_of_frames
                    self.direction = direction

                def GetCenter(self):
                    return self.rect.x + self.size // 2, self.rect.y + self.size // 2

                def GetPosition(self):
                    return self.rect.x, self.rect.y

                def SetPosition(self, position):
                    self.rect.x = position[0]
                    self.rect.y = position[1]

                def GetPointsOfMovement(self):
                    lst = [[self.rect.x, self.rect.y + self.size // 2],
                           [self.rect.x + self.size, self.rect.y + self.size],
                           [self.rect.x, self.rect.y + self.size],
                           [self.rect.x + self.size, self.rect.y + self.size // 2]]
                    return lst

                @abstractmethod
                def Attack(self, *args):
                    pass

            class RangeEnemy(Enemy):
                def __init__(self, spawn_position, health, size=kSizeOfEnemy):
                    super().__init__(spawn_position, health, size)
                    self.max_magic = 1000
                    self.magic_points = self.max_magic
                    self.last_fire_time = 1
                    self.cool_down = 3  # скорострельность оружия
                    self.max_distance = 1000  # расстояние, где противник может стрелять
                    self.ranged_attack_damage = 20
                    self.fires = []
                    self.dist = 300  # Рандомное число

                def Attack(self, player_position):
                    if time.time() - self.last_fire_time >= 1.5:  # проверяем прошло ли уже 1.5 секунды с прошлого выстрела
                        distance = math.sqrt(
                            (self.rect[0] - player_position[0]) ** 2 + (self.rect[1] - player_position[1]) ** 2)

                        if distance <= self.max_distance:
                            direction = [player_position[0] - self.rect.x, player_position[1] - self.rect.y]
                            fireball = Projectile(self.ranged_attack_damage, (self.rect.x, self.rect.y),
                                                  player_position,
                                                  distance, direction, 100, 0.5, magic_wizard)
                            self.fires.append(fireball)
                            self.magic_points -= 100
                            self.last_fire_time = time.time()

                    class RangeSkeleton(RangeEnemy):
                        def __init__(self, position):
                            super().__init__(position, HEALTH_OF_SKELETON, SIZE_OF_SKELETON)
